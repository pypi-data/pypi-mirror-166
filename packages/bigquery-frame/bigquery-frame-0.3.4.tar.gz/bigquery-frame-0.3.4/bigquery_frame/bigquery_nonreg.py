import difflib
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

from google.cloud.bigquery import SchemaField
from tqdm import tqdm

from bigquery_frame import BigQueryBuilder, DataFrame, bigquery_utils
from bigquery_frame import functions as f
from bigquery_frame import transformations as df_transformations
from bigquery_frame.auth import get_bq_client
from bigquery_frame.bigquery_utils import get_common_columns
from bigquery_frame.column import Column
from bigquery_frame.dataframe import cols_to_str, is_nullable, is_repeated
from bigquery_frame.transformations import analyze, union_dataframes
from bigquery_frame.transformations_impl.nested import canonize_arrays
from bigquery_frame.utils import (
    assert_true,
    quote,
    quote_columns,
    str_to_col,
    strip_margin,
)

DEFAULT_NB_DIFFED_ROWS = 10
DEFAULT_MAX_STRING_LENGTH = 30
DEFAULT_LEFT_DF_ALIAS = "left"
DEFAULT_RIGHT_DF_ALIAS = "right"

MAGIC_HASH_COL_NAME = "__MAGIC_HASH__"
EXISTS_COL_NAME = "__EXISTS__"
IS_EQUAL_COL_NAME = "__IS_EQUAL__"
STRUCT_SEPARATOR_ALPHA = "__DOT__"


class DataframeComparatorException(Exception):
    pass


class CombinatorialExplosionError(DataframeComparatorException):
    pass


@dataclass
class DiffStats:
    total: int
    """Total number of rows after joining the two DataFrames"""
    no_change: int
    """Number of rows that are identical in both DataFrames"""
    changed: int
    """Number of rows that are present in both DataFrames but that have different values"""
    in_left: int
    """Number of rows in the left DataFrame"""
    in_right: int
    """Number of rows in the right DataFrame"""
    only_in_left: int
    """Number of rows that are only present in the left DataFrame"""
    only_in_right: int
    """Number of rows that are only present in the right DataFrame"""

    @property
    def same_data(self) -> bool:
        return self.no_change == self.total

    @property
    def percent_changed(self) -> float:
        return round(self.changed * 100.0 / self.total, 2)

    @property
    def percent_no_change(self) -> float:
        return round(self.no_change * 100.0 / self.total, 2)

    @property
    def percent_only_in_left(self) -> float:
        return round(self.only_in_left * 100.0 / self.total, 2)

    @property
    def percent_only_in_right(self) -> float:
        return round(self.only_in_right * 100.0 / self.total, 2)


class _Predicates:
    present_in_both = f.col(f"{EXISTS_COL_NAME}.left_value") & f.col(f"{EXISTS_COL_NAME}.right_value")
    in_left = f.col(f"{EXISTS_COL_NAME}.left_value")
    in_right = f.col(f"{EXISTS_COL_NAME}.right_value")
    only_in_left = f.col(f"{EXISTS_COL_NAME}.left_value") & (f.col(f"{EXISTS_COL_NAME}.right_value") == f.lit(False))
    only_in_right = (f.col(f"{EXISTS_COL_NAME}.left_value") == f.lit(False)) & f.col(f"{EXISTS_COL_NAME}.right_value")
    row_is_equal = f.col(IS_EQUAL_COL_NAME)
    row_changed = f.col(IS_EQUAL_COL_NAME) == f.lit(False)


def _chunks(lst: List, n: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        # fmt: off
        yield lst[i: i + n]
        # fmt: on


def join_dataframes(*dfs: DataFrame, join_cols: List[str]) -> DataFrame:
    if len(dfs) == 1:
        return dfs[0]
    first_df = dfs[0]
    other_dfs = dfs[1:]
    excluded_common_cols = quote_columns(join_cols + [EXISTS_COL_NAME, IS_EQUAL_COL_NAME])
    is_equal = f.lit(True)
    for df in dfs:
        is_equal = is_equal & df[IS_EQUAL_COL_NAME]
    selected_columns = (
        str_to_col(join_cols)
        + [f.expr(f"{df._alias}.* EXCEPT ({cols_to_str(excluded_common_cols)})") for df in dfs]
        + [first_df[EXISTS_COL_NAME], is_equal.alias(IS_EQUAL_COL_NAME)]
    )
    on_str = ", ".join(join_cols)
    join_str = "\nJOIN ".join([f"{quote(df._alias)} USING ({on_str})" for df in other_dfs])

    query = strip_margin(
        f"""
        |SELECT
        |{cols_to_str(selected_columns, 2)}
        |FROM {quote(first_df._alias)}
        |JOIN {join_str}"""
    )
    return first_df._apply_query(query, deps=[first_df, *other_dfs])


class DiffResult:
    def __init__(self, same_schema: bool, diff_stats: DiffStats, diff_chunks: List[DataFrame], join_cols: List[str]):
        self.same_schema = same_schema
        self.diff_stats = diff_stats
        self.diff_chunks = diff_chunks
        self.join_cols = join_cols
        self._changed_df_chunks = None
        self._changed_df = None
        self._diff_df = None

    @property
    def same_data(self):
        return self.diff_stats.same_data

    @property
    def is_ok(self):
        return self.same_schema and self.same_data

    @property
    def diff_df(self):
        """The DataFrame containing all rows that were found in both DataFrames.
        WARNING: for very wide tables (~1000 columns) using this DataFrame might crash, and it is recommended
        to handle each diff_chunk separately"""
        if self._diff_df is None:
            self._diff_df = join_dataframes(*self.diff_chunks, join_cols=self.join_cols)
        return self._diff_df

    @property
    def changed_df(self):
        """The DataFrame containing all rows that were found in both DataFrames but are not equal"""
        if self._changed_df is None:
            self._changed_df = join_dataframes(*self.changed_df_chunks, join_cols=self.join_cols)
        return self._changed_df

    @property
    def changed_df_chunks(self):
        """The DataFrame containing all rows that were found in both DataFrames but are not equal"""
        if self._changed_df_chunks is None:
            self._changed_df_chunks = [
                df.filter(_Predicates.present_in_both & _Predicates.row_changed).drop(
                    EXISTS_COL_NAME, IS_EQUAL_COL_NAME
                )
                for df in self.diff_chunks
            ]
        return self._changed_df_chunks

    def __eq__(self, other):
        if isinstance(other, DiffResult):
            return self.same_schema == other.same_schema and self.diff_chunks == other.diff_chunks
        else:
            return NotImplemented

    def __repr__(self):
        return f"DiffResult(same_schema={self.same_schema}, diff_chunks={self.diff_chunks})"


class DataframeComparator:
    def __init__(
        self,
        nb_diffed_rows: int = DEFAULT_NB_DIFFED_ROWS,
        max_string_length: int = DEFAULT_MAX_STRING_LENGTH,
        left_df_alias: str = DEFAULT_LEFT_DF_ALIAS,
        right_df_alias: str = DEFAULT_RIGHT_DF_ALIAS,
        _chunk_size: Optional[int] = 100,
    ):
        self.nb_diffed_rows = nb_diffed_rows
        self.left_df_alias = left_df_alias
        self.right_df_alias = right_df_alias
        self.max_string_length = max_string_length
        self._chunk_size = _chunk_size
        pass

    @staticmethod
    def _canonize_col(col: Column, schema_field: SchemaField) -> Column:
        """Applies a transformation on the specified field depending on its type.
        This ensures that the hash of the column will be constant despite it's ordering.

        TODO: add doctests

        :param col: the SchemaField object
        :param schema_field: the parent DataFrame
        :return: a Column
        """
        if is_repeated(schema_field):
            col = f.expr(f"IF({col} IS NULL, NULL, TO_JSON_STRING({col}))")
        return col

    @staticmethod
    def _schema_to_string(
        schema: List[SchemaField], include_nullable: bool = False, include_metadata: bool = False
    ) -> List[str]:
        res = []
        for field in schema:
            s = f"{field.name} {field.field_type}"
            if include_nullable:
                if is_nullable(field):
                    s += " (nullable)"
                else:
                    s += " (required)"
            if include_metadata:
                s += f" {field.description}"
            res.append(s)
        return res

    @staticmethod
    def _compare_schemas(left_df: DataFrame, right_df: DataFrame) -> bool:
        """Compares two DataFrames schemas and print out the differences.
        Ignore the nullable and comment attributes.

        Example:

        >>> bq = BigQueryBuilder(get_bq_client())
        >>> left_df = bq.sql('''SELECT 1 as id, "" as c1, "" as c2, [STRUCT(2 as a, "" as b)] as c4''')
        >>> right_df = bq.sql('''SELECT 1 as id, 2 as c1, "" as c3, [STRUCT(3 as a, "" as d)] as c4''')
        >>> res = DataframeComparator._compare_schemas(left_df, right_df)
        Schema has changed:
        @@ -1,5 +1,5 @@
        <BLANKLINE>
         id INTEGER
        -c1 STRING
        -c2 STRING
        +c1 INTEGER
        +c3 STRING
         c4!.a INTEGER
        -c4!.b STRING
        +c4!.d STRING
        WARNING: columns that do not match both sides will be ignored
        >>> res
        False

        :param left_df: a DataFrame
        :param right_df: another DataFrame
        :return: True if both DataFrames have the same schema, False otherwise.
        """
        left_schema_flat = bigquery_utils.flatten_schema(left_df.schema, explode=True)
        right_schema_flat = bigquery_utils.flatten_schema(right_df.schema, explode=True)
        left_string_schema = DataframeComparator._schema_to_string(left_schema_flat)
        right_string_schema = DataframeComparator._schema_to_string(right_schema_flat)

        diff = list(difflib.unified_diff(left_string_schema, right_string_schema))[2:]

        if len(diff) > 0:
            print("Schema has changed:\n%s" % "\n".join(diff))
            print("WARNING: columns that do not match both sides will be ignored")
            return False
        else:
            print("Schema: ok (%s columns)" % len(left_df.columns))
            return True

    @staticmethod
    def _get_self_join_growth_estimate(df: DataFrame, cols: Union[str, List[str]]) -> float:
        """Computes how much time bigger a DataFrame will be if we self-join it using the provided columns,
        rounded to 2 decimals

        Example: If a DataFrame with 6 rows has one value present on 2 rows and another value present on 3 rows,
        the growth factor will be (1*1 + 2*2 + 3*3) / 6 ~= 2.33.
        If a column unique on each row, it's number of duplicates will be 0.

        >>> bq = BigQueryBuilder(get_bq_client())
        >>> df = bq.sql('''SELECT * FROM UNNEST([
        ...     STRUCT(1 as id, "a" as name),
        ...     STRUCT(2 as id, "b" as name),
        ...     STRUCT(3 as id, "b" as name),
        ...     STRUCT(4 as id, "c" as name),
        ...     STRUCT(5 as id, "c" as name),
        ...     STRUCT(6 as id, "c" as name)
        ... ])''')
        >>> DataframeComparator._get_self_join_growth_estimate(df, "id")
        1.0
        >>> DataframeComparator._get_self_join_growth_estimate(df, "name")
        2.33

        :param df: a DataFrame
        :param cols: a list of column names
        :return: number of duplicate rows
        """
        # TODO: rewrite with df.groupBy()
        if isinstance(cols, str):
            cols = [cols]
        query1 = strip_margin(
            f"""
        |SELECT
        |  COUNT(1) as nb
        |FROM {df._alias}
        |GROUP BY {cols_to_str(quote_columns(cols))}
        |"""
        )
        df1 = df._apply_query(query1)
        query2 = strip_margin(
            f"""
        |SELECT
        |  SUM(nb) as nb_rows,
        |  SUM(nb * nb) as nb_rows_after_self_join
        |FROM {df1._alias}
        |"""
        )
        df2 = df1._apply_query(query2)
        res = df2.take(1)[0]
        nb_rows = res.get("nb_rows")
        nb_rows_after_self_join = res.get("nb_rows_after_self_join")
        if nb_rows_after_self_join is None:
            nb_rows_after_self_join = 0
        if nb_rows is None or nb_rows == 0:
            return 1.0
        else:
            return round(nb_rows_after_self_join * 1.0 / nb_rows, 2)

    @staticmethod
    def _get_eligible_columns_for_join(df: DataFrame) -> Dict[str, float]:
        """Identifies the column with the least duplicates, in order to use it as the id for the comparison join.

        Eligible columns are all columns of type String, Int or Bigint that have an approximate distinct count of 90%
        of the number of rows in the DataFrame. Returns None if no such column is found.

        >>> bq = BigQueryBuilder(get_bq_client())
        >>> df = bq.sql('''SELECT * FROM UNNEST([
        ...     STRUCT(1 as id, "a" as name),
        ...     STRUCT(2 as id, "b" as name),
        ...     STRUCT(3 as id, "b" as name)
        ... ])''')
        >>> DataframeComparator._get_eligible_columns_for_join(df)
        {'id': 1.0}
        >>> df = bq.sql('''SELECT * FROM UNNEST([
        ...     STRUCT(1 as id, "a" as name),
        ...     STRUCT(1 as id, "a" as name)
        ... ])''')
        >>> DataframeComparator._get_eligible_columns_for_join(df)
        {}

        :param df: a DataFrame
        :return: The name of the columns with less than 10% duplicates, and their
            corresponding self-join-growth-estimate
        """
        eligible_cols = [
            col.name for col in df.schema if col.field_type in ["STRING", "INTEGER", "FLOAT"] and not is_repeated(col)
        ]
        if len(eligible_cols) == 0:
            return dict()
        distinct_count_threshold = f.lit(90.0)
        eligibility_df = df.select(
            [
                (
                    f.approx_count_distinct(quote(col)) * f.lit(100.0) / f.count(f.lit(1)) > distinct_count_threshold
                ).alias(col)
                for col in eligible_cols
            ]
        )
        columns_with_high_distinct_count = [key for key, value in eligibility_df.collect()[0].items() if value]
        cols_with_duplicates = {
            col: DataframeComparator._get_self_join_growth_estimate(df, col) for col in columns_with_high_distinct_count
        }
        return cols_with_duplicates

    @staticmethod
    def merge_growth_estimate_dicts(left_dict: Dict[str, float], right_dict: Dict[str, float]):
        """Merge together two dicts giving for each column name the corresponding growth_estimate

        >>> DataframeComparator.merge_growth_estimate_dicts({"a": 10.0, "b": 1.0}, {"a": 1.0, "c": 1.0})
        {'a': 5.5, 'b': 1.0, 'c': 1.0}

        :param left_dict:
        :param right_dict:
        :return:
        """
        res = left_dict.copy()
        for x in right_dict:
            if x in left_dict:
                res[x] = (res[x] + right_dict[x]) / 2
            else:
                res[x] = right_dict[x]
        return res

    @staticmethod
    def _automatically_infer_join_col(left_df: DataFrame, right_df: DataFrame) -> Tuple[Optional[str], Optional[float]]:
        """Identify the column with the least duplicates, in order to use it as the id for the comparison join.

        Eligible columns are all columns of type String, Int or Bigint that have an approximate distinct count of 90%
        of the number of rows in the DataFrame. Returns None if no suche column is found.

        >>> bq = BigQueryBuilder(get_bq_client())
        >>> left_df = bq.sql('''SELECT * FROM UNNEST([
        ...     STRUCT(1 as id, "a" as name),
        ...     STRUCT(2 as id, "b" as name),
        ...     STRUCT(3 as id, "c" as name),
        ...     STRUCT(4 as id, "d" as name),
        ...     STRUCT(5 as id, "e" as name),
        ...     STRUCT(6 as id, "f" as name)
        ... ])''')
        >>> right_df = bq.sql('''SELECT * FROM UNNEST([
        ...     STRUCT(1 as id, "a" as name),
        ...     STRUCT(2 as id, "a" as name),
        ...     STRUCT(3 as id, "b" as name),
        ...     STRUCT(4 as id, "c" as name),
        ...     STRUCT(5 as id, "d" as name),
        ...     STRUCT(6 as id, "e" as name)
        ... ])''')
        >>> DataframeComparator._automatically_infer_join_col(left_df, right_df)
        ('id', 1.0)
        >>> left_df = bq.sql('''SELECT * FROM UNNEST([
        ...     STRUCT(1 as id, "a" as name),
        ...     STRUCT(1 as id, "a" as name)
        ... ])''')
        >>> right_df = bq.sql('''SELECT * FROM UNNEST([
        ...     STRUCT(1 as id, "a" as name),
        ...     STRUCT(1 as id, "a" as name)
        ... ])''')
        >>> DataframeComparator._automatically_infer_join_col(left_df, right_df)
        (None, None)

        :param left_df: a DataFrame
        :param right_df: a DataFrame
        :return: The name of the column with the least duplicates in both DataFrames if it has less than 10% duplicates.
        """
        left_col_dict = DataframeComparator._get_eligible_columns_for_join(left_df)
        right_col_dict = DataframeComparator._get_eligible_columns_for_join(left_df)
        merged_col_dict = DataframeComparator.merge_growth_estimate_dicts(left_col_dict, right_col_dict)

        if len(merged_col_dict) > 0:
            col, self_join_growth_estimate = sorted(merged_col_dict.items(), key=lambda x: -x[1])[0]
            return col, self_join_growth_estimate
        else:
            return None, None

    @staticmethod
    def _build_diff_dataframe(left_df: DataFrame, right_df: DataFrame, join_cols: List[str]) -> DataFrame:
        """Perform a column-by-column comparison between two DataFrames.
        The two DataFrames must have the same columns with the same ordering.
        The column `join_col` will be used to join the two DataFrames together.
        Then we build a new DataFrame with the `join_col` and for each column, a struct with three elements:
        - `left_value`: the value coming from the `left_df`
        - `right_value`: the value coming from the `right_df`
        - `is_equal`: True if both values have the same hash, False otherwise.

        Example:

        >>> bq = BigQueryBuilder(get_bq_client())
        >>> left_df = bq.sql('''SELECT * FROM UNNEST([
        ...     STRUCT(1 as id, "a" as c1, 1 as c2),
        ...     STRUCT(2 as id, "b" as c1, 2 as c2),
        ...     STRUCT(3 as id, "c" as c1, 3 as c2)
        ... ])''')
        >>> right_df = bq.sql('''SELECT * FROM UNNEST([
        ...     STRUCT(1 as id, "a" as c1, 1 as c2),
        ...     STRUCT(2 as id, "b" as c1, 4 as c2),
        ...     STRUCT(4 as id, "f" as c1, 3 as c2)
        ... ])''')
        >>> left_df.show()
        +----+----+----+
        | id | c1 | c2 |
        +----+----+----+
        |  1 |  a |  1 |
        |  2 |  b |  2 |
        |  3 |  c |  3 |
        +----+----+----+
        >>> right_df.show()
        +----+----+----+
        | id | c1 | c2 |
        +----+----+----+
        |  1 |  a |  1 |
        |  2 |  b |  4 |
        |  4 |  f |  3 |
        +----+----+----+
        >>> DataframeComparator._build_diff_dataframe(left_df, right_df, ['id']).orderBy('id').show()
        +----+-------------------------------------------------------------+-----------------------------------------------------------+--------------------------------------------+--------------+
        | id |                                                          c1 |                                                        c2 |                                 __EXISTS__ | __IS_EQUAL__ |
        +----+-------------------------------------------------------------+-----------------------------------------------------------+--------------------------------------------+--------------+
        |  1 |   {'left_value': 'a', 'right_value': 'a', 'is_equal': True} |     {'left_value': 1, 'right_value': 1, 'is_equal': True} |  {'left_value': True, 'right_value': True} |         True |
        |  2 |   {'left_value': 'b', 'right_value': 'b', 'is_equal': True} |    {'left_value': 2, 'right_value': 4, 'is_equal': False} |  {'left_value': True, 'right_value': True} |        False |
        |  3 | {'left_value': 'c', 'right_value': None, 'is_equal': False} | {'left_value': 3, 'right_value': None, 'is_equal': False} | {'left_value': True, 'right_value': False} |        False |
        |  4 | {'left_value': None, 'right_value': 'f', 'is_equal': False} | {'left_value': None, 'right_value': 3, 'is_equal': False} | {'left_value': False, 'right_value': True} |        False |
        +----+-------------------------------------------------------------+-----------------------------------------------------------+--------------------------------------------+--------------+

        :param left_df: a DataFrame
        :param right_df: a DataFrame with the same columns
        :param join_cols: the columns to use to perform the join.
        :return: a DataFrame containing all the columns that differ, and a dictionary that gives the number of
            differing rows for each column
        """
        left_df = left_df.withColumn(EXISTS_COL_NAME, f.lit(True))
        right_df = right_df.withColumn(EXISTS_COL_NAME, f.lit(True))

        diff = left_df.join(right_df, join_cols, "full")

        compared_fields = [
            field for field in left_df.schema if field.name not in join_cols and field.name != EXISTS_COL_NAME
        ]

        def comparison_struct(field: SchemaField) -> Column:
            left_col: Column = left_df[field.name]
            right_col: Column = right_df[field.name]
            left_col_str: Column = DataframeComparator._canonize_col(left_col, field)
            right_col_str: Column = DataframeComparator._canonize_col(right_col, field)
            return f.struct(
                left_col.alias("left_value"),
                right_col.alias("right_value"),
                (
                    (left_col_str.isNull() & right_col_str.isNull())
                    | (left_col_str.isNotNull() & right_col_str.isNotNull() & (left_col_str == right_col_str))
                ).alias("is_equal"),
            ).alias(field.name)

        diff_df = diff.select(
            *[f.coalesce(left_df[col], right_df[col]).alias(col) for col in join_cols],
            *[comparison_struct(field) for field in compared_fields],
            f.struct(
                f.coalesce(left_df[EXISTS_COL_NAME], f.lit(False)).alias("left_value"),
                f.coalesce(right_df[EXISTS_COL_NAME], f.lit(False)).alias("right_value"),
            ).alias(EXISTS_COL_NAME),
        )

        row_is_equal = f.lit(True)
        for field in compared_fields:
            row_is_equal = row_is_equal & f.col(f"{field.name}.is_equal")
        return diff_df.withColumn(IS_EQUAL_COL_NAME, row_is_equal)

    def _get_join_cols(self, left_df: DataFrame, right_df: DataFrame, join_cols: List[str]) -> Tuple[List[str], float]:
        """Performs an in-depth analysis between two DataFrames with the same columns and prints the differences found.
        We first attempt to identify columns that look like ids.
        For that we choose all the columns with an approximate_count_distinct greater than 90% of the row count.
        For each column selected this way, we then perform a join and compare the DataFrames column by column.

        :param left_df: a DataFrame
        :param right_df: another DataFrame with the same columns
        :param join_cols: the list of columns on which to perform the join
        :return: a Dict that gives for each eligible join column the corresponding diff DataFrame
        """
        if join_cols is None:
            print(
                "No join_cols provided: "
                "trying to automatically infer a column that can be used for joining the two DataFrames"
            )
            inferred_join_col, self_join_growth_estimate = DataframeComparator._automatically_infer_join_col(
                left_df, right_df
            )
            if inferred_join_col is None:
                raise DataframeComparatorException(
                    "Could not automatically infer a column sufficiently "
                    "unique to join the two DataFrames and perform a comparison. "
                    "Please specify manually the columns to use with the join_cols parameter"
                )
            else:
                print(f"Found the following column: {inferred_join_col}")
                join_cols = [inferred_join_col]
        else:
            self_join_growth_estimate = (
                DataframeComparator._get_self_join_growth_estimate(left_df, join_cols)
                + DataframeComparator._get_self_join_growth_estimate(right_df, join_cols)
            ) / 2
        return join_cols, self_join_growth_estimate

    def _check_join_cols(
        self, specified_join_cols: Optional[List[str]], join_cols: Optional[List[str]], self_join_growth_estimate: float
    ) -> None:
        """Check the self_join_growth_estimate and raise an Exception if it is bigger than 2.

        This security helps to prevent users from accidentally spending huge query costs.
        Example: if a table has 10^9 rows and the join_col has a value with 10^6 duplicates, then the resulting
        self join will have (10^6)^2=10^12 which is 1000 times bigger than the original table.

        """
        inferred_provided_str = "provided"
        if specified_join_cols is None:
            inferred_provided_str = "inferred"
        if len(join_cols) == 1:
            plural_str = ""
            join_cols_str = str(join_cols[0])
        else:
            plural_str = "s"
            join_cols_str = str(join_cols)

        if self_join_growth_estimate >= 2.0:
            raise CombinatorialExplosionError(
                f"Performing a join with the {inferred_provided_str} column{plural_str} {join_cols_str} "
                f"would increase the size of the table by a factor of {self_join_growth_estimate}. "
                f"Please provide join_cols that are truly unique for both DataFrames."
            )
        print(
            f"We will try to find the differences by joining the DataFrames together "
            f"using the {inferred_provided_str} column{plural_str}: {join_cols_str}"
        )
        if self_join_growth_estimate > 1.0:
            print(
                f"WARNING: duplicates have been detected in the joining key, the resulting DataFrame "
                f"will be {self_join_growth_estimate} bigger which might affect the diff results. "
                f"Please consider providing join_cols that are truly unique for both DataFrames."
            )

    @staticmethod
    def _build_diff_per_column_df(unpivoted_diff_df: DataFrame, nb_diffed_rows) -> DataFrame:
        """Given an `unpivoted_diff_df` DataFrame, builds a DataFrame that gives for each columns the N most frequent
        differences that are happening, where N = `nb_diffed_rows`.

        Example:

        >>> bq = BigQueryBuilder(get_bq_client())
        >>> unpivoted_diff_df = bq.sql('''
        ...     SELECT * FROM UNNEST([
        ...         STRUCT(1 as id, "c1" as column, STRUCT("a" as left_value, "d" as right_value, False as is_equal) as diff),
        ...         STRUCT(1 as id, "c2" as column, STRUCT("x" as left_value, "x" as right_value, True as is_equal) as diff),
        ...         STRUCT(1 as id, "c3" as column, STRUCT("1" as left_value, "1" as right_value, True as is_equal) as diff),
        ...         STRUCT(2 as id, "c1" as column, STRUCT("b" as left_value, "a" as right_value, False as is_equal) as diff),
        ...         STRUCT(2 as id, "c2" as column, STRUCT("y" as left_value, "y" as right_value, True as is_equal) as diff),
        ...         STRUCT(2 as id, "c3" as column, STRUCT("2" as left_value, "4" as right_value, False as is_equal) as diff),
        ...         STRUCT(3 as id, "c1" as column, STRUCT("c" as left_value, "f" as right_value, False as is_equal) as diff),
        ...         STRUCT(3 as id, "c2" as column, STRUCT("z" as left_value, "z" as right_value, True as is_equal) as diff),
        ...         STRUCT(3 as id, "c3" as column, STRUCT("3" as left_value, "3" as right_value, True as is_equal) as diff)
        ...     ])
        ... ''')
        >>> unpivoted_diff_df.show()
        +----+--------+------------------------------------------------------------+
        | id | column |                                                       diff |
        +----+--------+------------------------------------------------------------+
        |  1 |     c1 | {'left_value': 'a', 'right_value': 'd', 'is_equal': False} |
        |  1 |     c2 |  {'left_value': 'x', 'right_value': 'x', 'is_equal': True} |
        |  1 |     c3 |  {'left_value': '1', 'right_value': '1', 'is_equal': True} |
        |  2 |     c1 | {'left_value': 'b', 'right_value': 'a', 'is_equal': False} |
        |  2 |     c2 |  {'left_value': 'y', 'right_value': 'y', 'is_equal': True} |
        |  2 |     c3 | {'left_value': '2', 'right_value': '4', 'is_equal': False} |
        |  3 |     c1 | {'left_value': 'c', 'right_value': 'f', 'is_equal': False} |
        |  3 |     c2 |  {'left_value': 'z', 'right_value': 'z', 'is_equal': True} |
        |  3 |     c3 |  {'left_value': '3', 'right_value': '3', 'is_equal': True} |
        +----+--------+------------------------------------------------------------+
        >>> DataframeComparator._build_diff_per_column_df(unpivoted_diff_df, 1).orderBy('column').show()
        +--------+------------+-------------+----------------+----------------------+
        | column | left_value | right_value | nb_differences | total_nb_differences |
        +--------+------------+-------------+----------------+----------------------+
        |     c1 |          a |           d |              1 |                    3 |
        |     c3 |          2 |           4 |              1 |                    1 |
        +--------+------------+-------------+----------------+----------------------+

        :param unpivoted_diff_df: a diff DataFrame
        :return: a dict that gives for each column with differences the number of rows with different values
          for this column
        """
        # We must make sure to break ties on nb_differences when ordering to ensure a deterministic for unit tests.
        # window = Window.partitionBy(f.col("column")).orderBy(
        #     f.col("nb_differences").desc(), f.col("left_value"), f.col("right_value")
        # )
        #
        # df = (
        #     unpivoted_diff_df.filter("diff.is_equal = false")
        #     .groupBy("column", "diff.left_value", "diff.right_value")
        #     .agg(f.count(f.lit(1)).alias("nb_differences"))
        #     .withColumn("row_num", f.row_number().over(window))
        #     .withColumn("total_nb_differences", f.sum("nb_differences").over(Window.partitionBy("column")))
        #     .where(f.col("row_num") <= f.lit(nb_diffed_rows))
        #     .drop("row_num")
        # )
        query1 = strip_margin(
            f"""
        |SELECT
        |  column,
        |  diff.left_value as left_value,
        |  diff.right_value as right_value,
        |  COUNT(1) as nb_differences
        |FROM {unpivoted_diff_df._alias}
        |WHERE diff.is_equal = false
        |GROUP BY column, diff.left_value, diff.right_value
        |"""
        )
        df1 = unpivoted_diff_df._apply_query(query1)

        query2 = strip_margin(
            f"""
        |SELECT
        |  column,
        |  left_value,
        |  right_value,
        |  nb_differences,
        |  SUM(nb_differences) OVER (PARTITION BY column) as total_nb_differences
        |FROM {df1._alias}
        |QUALIFY ROW_NUMBER() OVER (PARTITION BY column ORDER BY nb_differences DESC, left_value, right_value) <= {nb_diffed_rows} 
        |"""
        )
        df2 = df1._apply_query(query2)
        return df2.withColumn("column", f.replace(f.col("column"), STRUCT_SEPARATOR_ALPHA, "."), replace=True)

    def _unpivot(self, diff_df: DataFrame, join_cols: List[str]):
        """Given a diff_df, builds an unpivoted version of it.
        All the values must be cast to STRING to make sure everything fits in the same column.

        >>> diff_df = __get_test_intersection_diff_df()
        >>> diff_df.show()
        +----+------------------------------------------------------------+--------------------------------------------------------+
        | id |                                                         c1 |                                                     c2 |
        +----+------------------------------------------------------------+--------------------------------------------------------+
        |  1 | {'left_value': 'a', 'right_value': 'd', 'is_equal': False} |  {'left_value': 1, 'right_value': 1, 'is_equal': True} |
        |  2 | {'left_value': 'b', 'right_value': 'a', 'is_equal': False} | {'left_value': 2, 'right_value': 4, 'is_equal': False} |
        +----+------------------------------------------------------------+--------------------------------------------------------+
        >>> DataframeComparator()._unpivot(diff_df, join_cols=['id']).orderBy('id', 'column').show()
        +----+------------------------------------------------------------+--------+
        | id |                                                       diff | column |
        +----+------------------------------------------------------------+--------+
        |  1 | {'left_value': 'a', 'right_value': 'd', 'is_equal': False} |     c1 |
        |  1 |  {'left_value': '1', 'right_value': '1', 'is_equal': True} |     c2 |
        |  2 | {'left_value': 'b', 'right_value': 'a', 'is_equal': False} |     c1 |
        |  2 | {'left_value': '2', 'right_value': '4', 'is_equal': False} |     c2 |
        +----+------------------------------------------------------------+--------+

        :param diff_df:
        :param join_cols:
        :return:
        """

        def truncate_string(col):
            return f.when(
                f.length(col) > f.lit(self.max_string_length),
                f.concat(f.substring(col, 0, self.max_string_length - 3), f.lit("...")),
            ).otherwise(col)

        diff_df = diff_df.select(
            *quote_columns(join_cols),
            *[
                f.struct(
                    truncate_string(
                        DataframeComparator._canonize_col(diff_df[field.name + ".left_value"], field.fields[0]).cast(
                            "STRING"
                        )
                    ).alias("left_value"),
                    truncate_string(
                        DataframeComparator._canonize_col(diff_df[field.name + ".right_value"], field.fields[0]).cast(
                            "STRING"
                        )
                    ).alias("right_value"),
                    diff_df[quote(field.name) + ".is_equal"].alias("is_equal"),
                ).alias(field.name)
                for field in diff_df.schema
                if field.name not in join_cols
            ],
        )

        unpivot = df_transformations.unpivot(
            diff_df, pivot_columns=join_cols, key_alias="column", value_alias="diff", implem_version=2
        )
        return unpivot

    def _get_diff_stats(self, diff_chunks: List[DataFrame], join_cols: List[str]) -> DiffStats:
        """Given a diff_df and its list of join_cols, return stats about the number of differing or missing rows

        >>> _diff_df = __get_test_diff_df()
        >>> _diff_df.show()
        +----+-------------------------------------------------------------+-----------------------------------------------------------+--------------------------------------------+--------------+
        | id |                                                          c1 |                                                        c2 |                                 __EXISTS__ | __IS_EQUAL__ |
        +----+-------------------------------------------------------------+-----------------------------------------------------------+--------------------------------------------+--------------+
        |  1 |   {'left_value': 'a', 'right_value': 'a', 'is_equal': True} |     {'left_value': 1, 'right_value': 1, 'is_equal': True} |  {'left_value': True, 'right_value': True} |         True |
        |  2 |   {'left_value': 'b', 'right_value': 'b', 'is_equal': True} |    {'left_value': 2, 'right_value': 4, 'is_equal': False} |  {'left_value': True, 'right_value': True} |        False |
        |  3 | {'left_value': 'c', 'right_value': None, 'is_equal': False} | {'left_value': 3, 'right_value': None, 'is_equal': False} | {'left_value': True, 'right_value': False} |        False |
        |  4 | {'left_value': None, 'right_value': 'f', 'is_equal': False} | {'left_value': None, 'right_value': 3, 'is_equal': False} | {'left_value': False, 'right_value': True} |        False |
        +----+-------------------------------------------------------------+-----------------------------------------------------------+--------------------------------------------+--------------+
        >>> df_comparator = DataframeComparator(left_df_alias="before", right_df_alias="after")
        >>> df_comparator._get_diff_stats([_diff_df], join_cols=['id'])
        DiffStats(total=4, no_change=1, changed=1, in_left=3, in_right=3, only_in_left=1, only_in_right=1)
        >>> _diff_df_2 = _diff_df.select('id', f.col('c1').alias('c3'), f.col('c1').alias('c4'), EXISTS_COL_NAME, IS_EQUAL_COL_NAME)
        >>> df_comparator._get_diff_stats([_diff_df, _diff_df_2], join_cols=['id'])
        DiffStats(total=4, no_change=1, changed=1, in_left=3, in_right=3, only_in_left=1, only_in_right=1)

        :param diff_chunks: a list of diff_dataframe chunks
        :return:
        """
        diff_df = join_dataframes(*diff_chunks, join_cols=join_cols)
        res = diff_df.select(
            f.count(f.lit(1)).alias("total"),
            f.sum(f.when(_Predicates.present_in_both & _Predicates.row_is_equal, f.lit(1)).otherwise(f.lit(0))).alias(
                "no_change"
            ),
            f.sum(f.when(_Predicates.present_in_both & _Predicates.row_changed, f.lit(1)).otherwise(f.lit(0))).alias(
                "changed"
            ),
            f.sum(f.when(_Predicates.in_left, f.lit(1)).otherwise(f.lit(0))).alias("in_left"),
            f.sum(f.when(_Predicates.in_right, f.lit(1)).otherwise(f.lit(0))).alias("in_right"),
            f.sum(f.when(_Predicates.only_in_left, f.lit(1)).otherwise(f.lit(0))).alias("only_in_left"),
            f.sum(f.when(_Predicates.only_in_right, f.lit(1)).otherwise(f.lit(0))).alias("only_in_right"),
        ).collect()
        return DiffStats(**{k: (v if v is not None else 0) for k, v in res[0].items()})

    def _get_diff_count_per_col(self, diff_df: DataFrame, join_cols: List[str]) -> DataFrame:
        """Given a diff_df and its list of join_cols, return a DataFrame with the following properties:

        - One row per "diff tuple" (col_name, col_value_left, col_value_right)
        - A column nb_differences that gives the number of occurrence of each "diff tuple"
        - A column total_nb_differences that gives total number of differences found for this col_name.

        >>> _diff_df = __get_test_intersection_diff_df()
        >>> _diff_df.show()
        +----+------------------------------------------------------------+--------------------------------------------------------+
        | id |                                                         c1 |                                                     c2 |
        +----+------------------------------------------------------------+--------------------------------------------------------+
        |  1 | {'left_value': 'a', 'right_value': 'd', 'is_equal': False} |  {'left_value': 1, 'right_value': 1, 'is_equal': True} |
        |  2 | {'left_value': 'b', 'right_value': 'a', 'is_equal': False} | {'left_value': 2, 'right_value': 4, 'is_equal': False} |
        +----+------------------------------------------------------------+--------------------------------------------------------+
        >>> df_comparator = DataframeComparator(left_df_alias="before", right_df_alias="after")
        >>> df_comparator._get_diff_count_per_col(_diff_df, join_cols = ['id']).show()
        +--------+------------+-------------+----------------+----------------------+
        | column | left_value | right_value | nb_differences | total_nb_differences |
        +--------+------------+-------------+----------------+----------------------+
        |     c1 |          a |           d |              1 |                    2 |
        |     c1 |          b |           a |              1 |                    2 |
        |     c2 |          2 |           4 |              1 |                    1 |
        +--------+------------+-------------+----------------+----------------------+

        :param diff_df:
        :param join_cols:
        :return:
        """
        unpivoted_diff_df = self._unpivot(diff_df, join_cols)
        unpivoted_diff_df = unpivoted_diff_df.where("NOT COALESCE(diff.is_equal, FALSE)")
        diff_count_per_col_df = DataframeComparator._build_diff_per_column_df(
            unpivoted_diff_df, self.nb_diffed_rows
        ).orderBy("column")
        return diff_count_per_col_df

    def _get_diff_count_per_col_for_chunks(self, diff_chunks: List[DataFrame], join_cols: List[str]) -> DataFrame:
        diff_count_per_col_df_chunks = [
            self._get_diff_count_per_col(diff_df, join_cols).persist() for diff_df in tqdm(diff_chunks)
        ]
        return union_dataframes(diff_count_per_col_df_chunks)

    def _display_diff_results(self, diff_count_per_col_df: DataFrame):
        """Displays the results of the diff analysis.
        We first display the a summary of all columns that changed with the number of changes,
        then for each column, we display a summary of the most frequent changes and then
        we display examples of rows where this column changed, along with all the other columns
        that changed in this diff.

        Example:

        >>> bq = BigQueryBuilder(get_bq_client())
        >>> diff_count_per_col_df = bq.sql('''
        ...     SELECT * FROM UNNEST([
        ...         STRUCT('c1' as column, 'a' as left_value, 'd' as right_value, 1 as nb_differences, 3 as total_nb_differences),
        ...         STRUCT('c3' as column, '2' as left_value, '4' as right_value, 1 as nb_differences, 1 as total_nb_differences)
        ... ])''')
        >>> diff_count_per_col_df.show()
        +--------+------------+-------------+----------------+----------------------+
        | column | left_value | right_value | nb_differences | total_nb_differences |
        +--------+------------+-------------+----------------+----------------------+
        |     c1 |          a |           d |              1 |                    3 |
        |     c3 |          2 |           4 |              1 |                    1 |
        +--------+------------+-------------+----------------+----------------------+
        >>> df_comparator = DataframeComparator(left_df_alias="before", right_df_alias="after")
        >>> df_comparator._display_diff_results(diff_count_per_col_df)
        Found the following differences:
        +-------------+---------------+--------+-------+----------------+
        | column_name | total_nb_diff | before | after | nb_differences |
        +-------------+---------------+--------+-------+----------------+
        |          c1 |             3 |      a |     d |              1 |
        |          c3 |             1 |      2 |     4 |              1 |
        +-------------+---------------+--------+-------+----------------+

        :param diff_count_per_col_df:
        :return:
        """
        print(f"Found the following differences:")
        diff_count_per_col_df.select(
            f.col("column").alias("`column_name`"),
            f.col("total_nb_differences").alias("`total_nb_diff`"),
            f.col("left_value").alias(quote(self.left_df_alias)),
            f.col("right_value").alias(quote(self.right_df_alias)),
            f.col("nb_differences").alias("`nb_differences`"),
        ).show(1000 * self.nb_diffed_rows)

    def _format_diff_df(self, join_cols: List[str], diff_df: DataFrame) -> DataFrame:
        """Given a diff DataFrame, rename the columns to prefix them with the left_df_alias and right_df_alias.

        :param join_cols:
        :param diff_df:
        :return:
        """
        return diff_df.select(
            *quote_columns(join_cols),
            *[
                col
                for col_name in diff_df.columns
                if col_name not in join_cols
                for col in [
                    diff_df[quote(col_name)]["left_value"].alias(f"{self.left_df_alias}__{col_name}"),
                    diff_df[quote(col_name)]["right_value"].alias(f"{self.right_df_alias}__{col_name}"),
                ]
            ],
        )

    def _display_diff_examples(self, diff_df: DataFrame, diff_count_per_col_df: DataFrame, join_cols: List[str]):
        """For each column that has differences, print examples of rows where such a difference occurs.

        >>> _diff_df = __get_test_intersection_diff_df()
        >>> _diff_df.show()
        +----+------------------------------------------------------------+--------------------------------------------------------+
        | id |                                                         c1 |                                                     c2 |
        +----+------------------------------------------------------------+--------------------------------------------------------+
        |  1 | {'left_value': 'a', 'right_value': 'd', 'is_equal': False} |  {'left_value': 1, 'right_value': 1, 'is_equal': True} |
        |  2 | {'left_value': 'b', 'right_value': 'a', 'is_equal': False} | {'left_value': 2, 'right_value': 4, 'is_equal': False} |
        +----+------------------------------------------------------------+--------------------------------------------------------+
        >>> df_comparator = DataframeComparator(left_df_alias="before", right_df_alias="after")
        >>> _diff_count_per_col_df = df_comparator._get_diff_count_per_col(_diff_df, join_cols = ['id'])
        >>> df_comparator._display_diff_examples(_diff_df, _diff_count_per_col_df, join_cols = ['id'])
        Detailed examples :
        'c1' : 2 rows
        +----+------------+-----------+------------+-----------+
        | id | before__c1 | after__c1 | before__c2 | after__c2 |
        +----+------------+-----------+------------+-----------+
        |  1 |          a |         d |          1 |         1 |
        |  2 |          b |         a |          2 |         4 |
        +----+------------+-----------+------------+-----------+
        'c2' : 1 rows
        +----+------------+-----------+------------+-----------+
        | id | before__c1 | after__c1 | before__c2 | after__c2 |
        +----+------------+-----------+------------+-----------+
        |  2 |          b |         a |          2 |         4 |
        +----+------------+-----------+------------+-----------+

        :param diff_df:
        :param diff_count_per_col_df:
        :param join_cols:
        :return:
        """
        rows = diff_count_per_col_df.select("column", "total_nb_differences").distinct().collect()
        diff_count_per_col = [(r[0], r[1]) for r in rows]
        print("Detailed examples :")
        for col, nb in diff_count_per_col:
            print(f"'{col}' : {nb} rows")
            rows_that_changed_for_that_column = diff_df.filter(~diff_df[quote(col)]["is_equal"]).select(
                *join_cols, *[quote(r[0]) for r in rows]
            )
            self._format_diff_df(join_cols, rows_that_changed_for_that_column).show(self.nb_diffed_rows)

    def _get_side_diff_df(self, diff_df: DataFrame, side: str, join_cols: List[str]) -> DataFrame:
        """Given a diff_df, compute the set of all values present only on the specified side.

        >>> _diff_df = __get_test_diff_df()
        >>> _diff_df.show()
        +----+-------------------------------------------------------------+-----------------------------------------------------------+--------------------------------------------+--------------+
        | id |                                                          c1 |                                                        c2 |                                 __EXISTS__ | __IS_EQUAL__ |
        +----+-------------------------------------------------------------+-----------------------------------------------------------+--------------------------------------------+--------------+
        |  1 |   {'left_value': 'a', 'right_value': 'a', 'is_equal': True} |     {'left_value': 1, 'right_value': 1, 'is_equal': True} |  {'left_value': True, 'right_value': True} |         True |
        |  2 |   {'left_value': 'b', 'right_value': 'b', 'is_equal': True} |    {'left_value': 2, 'right_value': 4, 'is_equal': False} |  {'left_value': True, 'right_value': True} |        False |
        |  3 | {'left_value': 'c', 'right_value': None, 'is_equal': False} | {'left_value': 3, 'right_value': None, 'is_equal': False} | {'left_value': True, 'right_value': False} |        False |
        |  4 | {'left_value': None, 'right_value': 'f', 'is_equal': False} | {'left_value': None, 'right_value': 3, 'is_equal': False} | {'left_value': False, 'right_value': True} |        False |
        +----+-------------------------------------------------------------+-----------------------------------------------------------+--------------------------------------------+--------------+
        >>> df_comparator = DataframeComparator(left_df_alias="before", right_df_alias="after")
        >>> df_comparator._get_side_diff_df(_diff_df, side="left", join_cols=["id"]).show()
        +----+----+----+
        | id | c1 | c2 |
        +----+----+----+
        |  3 |  c |  3 |
        +----+----+----+
        >>> df_comparator._get_side_diff_df(_diff_df, side="right", join_cols=["id"]).show()
        +----+----+----+
        | id | c1 | c2 |
        +----+----+----+
        |  4 |  f |  3 |
        +----+----+----+

        :param diff_df:
        :return:
        """
        assert_true(side in ["left", "right"])
        if side == "left":
            predicate = _Predicates.only_in_left
        else:
            predicate = _Predicates.only_in_right
        df = diff_df.filter(predicate).drop(EXISTS_COL_NAME, IS_EQUAL_COL_NAME)
        compared_cols = [
            f.col(f"{field.name}.{side}_value").alias(field.name) for field in df.schema if field.name not in join_cols
        ]
        return df.select(*join_cols, *compared_cols)

    def _print_diff_stats(self, diff_stats: DiffStats):
        if diff_stats.total == diff_stats.no_change:
            print("\ndiff ok!\n")
        else:
            print("\ndiff NOT ok\n")
            print("Summary:")
            nb_row_diff = diff_stats.in_right - diff_stats.in_left
            if nb_row_diff != 0:
                if nb_row_diff > 0:
                    more_less = "more"
                else:
                    more_less = "less"
                print("\nRow count changed: ")
                print(f"{self.left_df_alias}: {diff_stats.in_left} rows")
                print(f"{self.right_df_alias}: {diff_stats.in_right} rows ({abs(nb_row_diff)} {more_less})")
                print("")
            else:
                print(f"\nRow count ok: {diff_stats.in_right} rows")
                print("")
            print(f"{diff_stats.no_change} ({diff_stats.percent_no_change}%) rows are identical")
            print(f"{diff_stats.changed} ({diff_stats.percent_changed}%) rows have changed")
            if diff_stats.only_in_left > 0:
                print(
                    f"{diff_stats.only_in_left} ({diff_stats.percent_only_in_left}%) rows are only in '{self.left_df_alias}'"
                )
            if diff_stats.only_in_right > 0:
                print(
                    f"{diff_stats.only_in_right} ({diff_stats.percent_only_in_right}%) rows are only in '{self.right_df_alias}"
                )
            print("")

    def _build_diff_dataframe_for_chunk(
        self,
        left_flat: DataFrame,
        right_flat: DataFrame,
        common_column_chunk: List[Tuple[str, str]],
        join_cols: List[str],
        skip_make_dataframes_comparable: bool,
    ):
        if not skip_make_dataframes_comparable:
            left_flat, right_flat = bigquery_utils.make_dataframes_comparable(
                left_flat, right_flat, common_column_chunk
            )
        left_flat = canonize_arrays(left_flat)
        right_flat = canonize_arrays(right_flat)
        return self._build_diff_dataframe(left_flat, right_flat, join_cols)

    def _build_diff_dataframe_chunks(
        self,
        left_df: DataFrame,
        right_df: DataFrame,
        common_columns: List[Tuple[str, str]],
        join_cols: List[str],
        same_schema: bool,
    ) -> List[DataFrame]:
        """TODO

        >>> bq = BigQueryBuilder(get_bq_client())
        >>> left_df = bq.sql('''SELECT * FROM UNNEST([
        ...     STRUCT(1 as id, "a" as c1, 1 as c2),
        ...     STRUCT(2 as id, "b" as c1, 2 as c2),
        ...     STRUCT(3 as id, "c" as c1, 3 as c2)
        ... ])''')
        >>> right_df = bq.sql('''SELECT * FROM UNNEST([
        ...     STRUCT(1 as id, "a" as c1, 1 as c2),
        ...     STRUCT(2 as id, "b" as c1, 4 as c2),
        ...     STRUCT(4 as id, "f" as c1, 3 as c2)
        ... ])''')
        >>> left_df.show()
        +----+----+----+
        | id | c1 | c2 |
        +----+----+----+
        |  1 |  a |  1 |
        |  2 |  b |  2 |
        |  3 |  c |  3 |
        +----+----+----+
        >>> right_df.show()
        +----+----+----+
        | id | c1 | c2 |
        +----+----+----+
        |  1 |  a |  1 |
        |  2 |  b |  4 |
        |  4 |  f |  3 |
        +----+----+----+
        >>> chunks = DataframeComparator(_chunk_size=10)._build_diff_dataframe_chunks(left_df, right_df,[('id', None), ('c1', None), ('c2', None)],['id'], same_schema=True)
        >>> for chunk in chunks: chunk.orderBy('id').show()
        +----+-------------------------------------------------------------+-----------------------------------------------------------+--------------------------------------------+--------------+
        | id |                                                          c1 |                                                        c2 |                                 __EXISTS__ | __IS_EQUAL__ |
        +----+-------------------------------------------------------------+-----------------------------------------------------------+--------------------------------------------+--------------+
        |  1 |   {'left_value': 'a', 'right_value': 'a', 'is_equal': True} |     {'left_value': 1, 'right_value': 1, 'is_equal': True} |  {'left_value': True, 'right_value': True} |         True |
        |  2 |   {'left_value': 'b', 'right_value': 'b', 'is_equal': True} |    {'left_value': 2, 'right_value': 4, 'is_equal': False} |  {'left_value': True, 'right_value': True} |        False |
        |  3 | {'left_value': 'c', 'right_value': None, 'is_equal': False} | {'left_value': 3, 'right_value': None, 'is_equal': False} | {'left_value': True, 'right_value': False} |        False |
        |  4 | {'left_value': None, 'right_value': 'f', 'is_equal': False} | {'left_value': None, 'right_value': 3, 'is_equal': False} | {'left_value': False, 'right_value': True} |        False |
        +----+-------------------------------------------------------------+-----------------------------------------------------------+--------------------------------------------+--------------+
        >>> chunks = DataframeComparator(_chunk_size=1)._build_diff_dataframe_chunks(left_df, right_df,[('id', None), ('c1', None), ('c2', None)],['id'], same_schema=False)
        >>> for chunk in chunks: chunk.orderBy('id').show()
        +----+-------------------------------------------------------------+--------------------------------------------+--------------+
        | id |                                                          c1 |                                 __EXISTS__ | __IS_EQUAL__ |
        +----+-------------------------------------------------------------+--------------------------------------------+--------------+
        |  1 |   {'left_value': 'a', 'right_value': 'a', 'is_equal': True} |  {'left_value': True, 'right_value': True} |         True |
        |  2 |   {'left_value': 'b', 'right_value': 'b', 'is_equal': True} |  {'left_value': True, 'right_value': True} |         True |
        |  3 | {'left_value': 'c', 'right_value': None, 'is_equal': False} | {'left_value': True, 'right_value': False} |        False |
        |  4 | {'left_value': None, 'right_value': 'f', 'is_equal': False} | {'left_value': False, 'right_value': True} |        False |
        +----+-------------------------------------------------------------+--------------------------------------------+--------------+
        +----+-----------------------------------------------------------+--------------------------------------------+--------------+
        | id |                                                        c2 |                                 __EXISTS__ | __IS_EQUAL__ |
        +----+-----------------------------------------------------------+--------------------------------------------+--------------+
        |  1 |     {'left_value': 1, 'right_value': 1, 'is_equal': True} |  {'left_value': True, 'right_value': True} |         True |
        |  2 |    {'left_value': 2, 'right_value': 4, 'is_equal': False} |  {'left_value': True, 'right_value': True} |        False |
        |  3 | {'left_value': 3, 'right_value': None, 'is_equal': False} | {'left_value': True, 'right_value': False} |        False |
        |  4 | {'left_value': None, 'right_value': 3, 'is_equal': False} | {'left_value': False, 'right_value': True} |        False |
        +----+-----------------------------------------------------------+--------------------------------------------+--------------+

        :param left_df: a DataFrame
        :param right_df: a DataFrame with the same columns
        :param join_cols: the columns to use to perform the join.
        :return: a DataFrame containing all the columns that differ, and a dictionary that gives the number of
            differing rows for each column
        """
        join_columns = [(col, tpe) for (col, tpe) in common_columns if col in join_cols]
        non_join_columns = [(col, tpe) for (col, tpe) in common_columns if col not in join_cols]
        nb_cols = len(non_join_columns)

        if nb_cols <= self._chunk_size:
            return [
                self._build_diff_dataframe_for_chunk(
                    left_df, right_df, common_columns, join_cols, skip_make_dataframes_comparable=same_schema
                ).persist()
            ]
        else:
            columns_chunk = [join_columns + chunk for chunk in _chunks(non_join_columns, self._chunk_size)]
            dfs = [
                self._build_diff_dataframe_for_chunk(
                    left_df, right_df, column_chunk, join_cols, skip_make_dataframes_comparable=False
                ).persist()
                for column_chunk in tqdm(columns_chunk)
            ]
            return dfs

    def compare_df(
        self, left_df: DataFrame, right_df: DataFrame, join_cols: List[str] = None, show_examples: bool = False
    ) -> DiffResult:
        """Compares two DataFrames and print out the differences.
        We first compare the DataFrame schemas. If the schemas are different, we adapt the DataFrames to make them
        as much comparable as possible:
        - If the column ordering changed, we re-order them
        - If a column type changed, we cast the column to the smallest common type
        - If a column was added, removed or renamed, it will be ignored.

        If `join_cols` is specified, we will use the specified columns to perform the comparison join between the
        two DataFrames. Ideally, the `join_cols` should respect an unicity constraint.
        If they contain duplicates, a safety check is performed to prevent a potential combinatorial explosion:
        if the number of rows in the joined DataFrame would be more than twice the size of the original DataFrames,
        then an Exception is raised and the user will be asked to provide another set of `join_cols`.

        If no `join_cols` is specified, the algorithm will try to automatically find a single column suitable for
        the join. However, the automatic inference can only find join keys based on a single column.
        If the DataFrame's unique keys are composite (multiple columns) they must be given explicitly via `join_cols`
        to perform the diff analysis.

        Tips:
        -----
        - If you want to test a column renaming, you can temporarily add renaming step to the DataFrame you want to test.
        - When comparing arrays, this algorithm ignores their ordering (e.g. `[1, 2, 3] == [3, 2, 1]`)
        - The algorithm is able to handle nested non-repeated records, such as STRUCT<STRUCT<>>, or even ARRAY<STRUCT>>
          but it doesn't support nested repeated structures, such as ARRAY<STRUCT<ARRAY<>>>.

        :param left_df: a DataFrame
        :param right_df: another DataFrame
        :param join_cols: [Optional] specifies the columns on which the two DataFrames should be joined to compare them
        :param show_examples: if set to True, print for each column examples of full rows where this column changes
        :return: a DiffResult object
        """
        if join_cols == []:
            join_cols = None
        specified_join_cols = join_cols

        # nb_cols = len(left_flat_schema) + len(right_flat_schema)
        # should_persist = nb_cols > 200
        same_schema = self._compare_schemas(left_df, right_df)

        left_flat = df_transformations.flatten(left_df, struct_separator=STRUCT_SEPARATOR_ALPHA)
        right_flat = df_transformations.flatten(right_df, struct_separator=STRUCT_SEPARATOR_ALPHA)

        print("\nAnalyzing differences...")
        join_cols, self_join_growth_estimate = self._get_join_cols(left_flat, right_flat, join_cols)
        self._check_join_cols(specified_join_cols, join_cols, self_join_growth_estimate)

        left_schema_flat = bigquery_utils.flatten_schema(left_df.schema, explode=True)
        if not same_schema:
            # We apply a `limit(0).persist()` to prevent BigQuery from crashing on very large tables
            right_schema_flat = bigquery_utils.flatten_schema(right_df.schema, explode=True)
            common_columns = get_common_columns(left_schema_flat, right_schema_flat)
        else:
            common_columns = [(field.name, None) for field in left_schema_flat]

        diff_chunks = self._build_diff_dataframe_chunks(left_flat, right_flat, common_columns, join_cols, same_schema)

        diff_stats: DiffStats = self._get_diff_stats(diff_chunks, join_cols)
        diff_result = DiffResult(same_schema, diff_stats, diff_chunks, join_cols)
        self._print_diff_stats(diff_stats)
        if diff_stats.changed > 0:
            diff_count_per_col_df = self._get_diff_count_per_col_for_chunks(diff_result.changed_df_chunks, join_cols)
            self._display_diff_results(diff_count_per_col_df)
            if show_examples:
                self._display_diff_examples(diff_result.diff_df, diff_count_per_col_df, join_cols)

        if diff_stats.only_in_left > 0:
            left_only_df = self._get_side_diff_df(diff_result.diff_df, "left", join_cols)
            print(f"{diff_stats.only_in_left} rows were only found in '{self.left_df_alias}' :")
            analyze(left_only_df).show(len(left_only_df.schema))

        if diff_stats.only_in_right > 0:
            right_only_df = self._get_side_diff_df(diff_result.diff_df, "right", join_cols)
            print(f"{diff_stats.only_in_right} rows were only found in '{self.right_df_alias}':")
            analyze(right_only_df).show(len(right_only_df.schema))

        return diff_result


def __get_test_diff_df() -> DataFrame:
    bq = BigQueryBuilder(get_bq_client())
    diff_df = bq.sql(
        """
        SELECT * FROM UNNEST([
            STRUCT(
                1 as id,
                STRUCT("a" as left_value, "a" as right_value, True as is_equal) as c1,
                STRUCT(1 as left_value, 1 as right_value, True as is_equal) as c2,
                STRUCT(True as left_value, True as right_value) as __EXISTS__,
                TRUE as __IS_EQUAL__
            ),
            STRUCT(
                2 as id,
                STRUCT("b" as left_value, "b" as right_value, True as is_equal) as c1,
                STRUCT(2 as left_value, 4 as right_value, False as is_equal) as c2,
                STRUCT(True as left_value, True as right_value) as __EXISTS__,
                FALSE as __IS_EQUAL__
            ),
            STRUCT(
                3 as id,
                STRUCT("c" as left_value, NULL as right_value, False as is_equal) as c1,
                STRUCT(3 as left_value, NULL as right_value, False as is_equal) as c2,
                STRUCT(True as left_value, False as right_value) as __EXISTS__,
                FALSE as __IS_EQUAL__
            ),
            STRUCT(
                4 as id,
                STRUCT(NULL as left_value, "f" as right_value, False as is_equal) as c1,
                STRUCT(NULL as left_value, 3 as right_value, False as is_equal) as c2,
                STRUCT(False as left_value, True as right_value) as __EXISTS__,
                FALSE as __IS_EQUAL__
            )
        ])
    """
    )
    return diff_df


def __get_test_intersection_diff_df() -> DataFrame:
    bq = BigQueryBuilder(get_bq_client())
    diff_df = bq.sql(
        """
        SELECT * FROM UNNEST([
            STRUCT(
                1 as id,
                STRUCT("a" as left_value, "d" as right_value, False as is_equal) as c1,
                STRUCT(1 as left_value, 1 as right_value, True as is_equal) as c2
            ),
            STRUCT(
                2 as id,
                STRUCT("b" as left_value, "a" as right_value, False as is_equal) as c1,
                STRUCT(2 as left_value, 4 as right_value, False as is_equal) as c2
            )
        ])
    """
    )
    return diff_df


# TODO: add functions.TO_BASE64
# TODO: add caching of DataFrames by SQL query
# TODO: add functions.asc/desc and Column.asc/desc
# TODO: add bq.createDataFrame()
# TODO: add support for Window functions (row_number)
# TODO: add support for groupBy
# TODO: f.col("s")["a"] should work
# TODO: analyze crashes when doing a group_by on a column if a column with the same name exists inside a struct
