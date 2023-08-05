from collections import OrderedDict
from typing import Dict, Iterable, List, Optional, Union

from bigquery_frame import BigQueryBuilder, DataFrame
from bigquery_frame import functions as f
from bigquery_frame.auth import get_bq_client
from bigquery_frame.column import Column
from bigquery_frame.dataframe import cols_to_str, strip_margin
from bigquery_frame.functions import StringOrColumn
from bigquery_frame.transformations_impl.flatten import flatten_schema
from bigquery_frame.utils import quote, str_to_col

OrderedTree = Union["OrderedTree", Dict[str, "OrderedTree"]]

# TODO: move this somewhere else
ELEMENT_COL_NAME = "_"
STRUCT_SEPARATOR = "."
REPETITION_MARKER = "!"


def transform(array: StringOrColumn, transform_col: Column, sort_cols: Optional[Union[Column, List[Column]]] = None):
    """TODO: document

    >>> transform_col = f.struct((f.col("a") + f.col("b")).alias("c"), (f.col("a") - f.col("b")).alias("d"))
    >>> order_cols = [f.col("a"), f.col("b")]
    >>> transform("s", transform_col, order_cols)
    Column('ARRAY(
      SELECT
        STRUCT((`a`) + (`b`) as `c`, (`a`) - (`b`) as `d`)
      FROM UNNEST(`s`) as `_`
      ORDER BY `a`, `b`
    )')

    >>> transform("s", f.col("_").cast("STRING"))
    Column('ARRAY(
      SELECT
        CAST(`_` as STRING)
      FROM UNNEST(`s`) as `_`
    )')

    >>> transform("s", f.col("_").cast("STRING"), sort_cols=f.col("_"))
    Column('ARRAY(
      SELECT
        CAST(`_` as STRING)
      FROM UNNEST(`s`) as `_`
      ORDER BY `_`
    )')

    >>> transform("s", f.col("_").cast("STRING"), sort_cols=f.col("_").desc())
    Column('ARRAY(
      SELECT
        CAST(`_` as STRING)
      FROM UNNEST(`s`) as `_`
      ORDER BY `_` DESC
    )')

    >>> x = f.col("_")
    >>> transform_col = f.struct((x["a"] + x["b"]).alias("c"), (x["a"] - x["b"]).alias("d"))
    >>> sort_col = [x["a"], x["b"]]
    >>> transform("s", transform_col, sort_col)
    Column('ARRAY(
      SELECT
        STRUCT((`_`.`a`) + (`_`.`b`) as `c`, (`_`.`a`) - (`_`.`b`) as `d`)
      FROM UNNEST(`s`) as `_`
      ORDER BY `_`.`a`, `_`.`b`
    )')

    :param array:
    :param transform_col:
    :param sort_cols:
    :return:
    """
    array = str_to_col(array)
    sort_str = ""
    if sort_cols is not None:
        if not isinstance(sort_cols, Iterable):
            sort_cols = [sort_cols]
        sort_str = f"\n  ORDER BY {', '.join([col.expr for col in sort_cols])}"

    return Column(
        strip_margin(
            f"""
            |ARRAY(
            |  SELECT
            |    {transform_col}
            |  FROM UNNEST({array}) as {quote(ELEMENT_COL_NAME)}{sort_str}
            |)"""
        )
    )


def _build_nested_struct_tree(columns: Dict[str, Column]) -> OrderedTree:
    def rec_insert(node: OrderedDict, alias: str, column: Column) -> None:
        if STRUCT_SEPARATOR in alias:
            struct, subcol = alias.split(STRUCT_SEPARATOR, 1)
            if struct not in node:
                node[struct] = OrderedDict()
            rec_insert(node[struct], subcol, column)
        else:
            node[alias] = column

    tree = OrderedDict()
    for col_name, col_type in columns.items():
        rec_insert(tree, col_name, col_type)
    return tree


def _build_struct_from_tree(node: OrderedTree, sort: bool = False) -> List[Column]:
    """

    >>> tree = OrderedDict([('s!', OrderedDict([('c', f.col("c")), ('d', f.col("d").cast("FLOAT64"))]))])
    >>> for c in _build_struct_from_tree(tree): print(c)
    ARRAY(
      SELECT
        STRUCT(`c` as `c`, CAST(`d` as FLOAT64) as `d`)
      FROM UNNEST(s) as `_`
    ) as `s`

    >>> tree = OrderedDict([('s', OrderedDict([('e!', f.col("_").cast("FLOAT64"))]))])
    >>> for c in _build_struct_from_tree(tree): print(c)
    STRUCT(ARRAY(
      SELECT
        CAST(`_` as FLOAT64)
      FROM UNNEST(`s`.`e`) as `_`
    ) as `e`) as `s`

    >>> tree = OrderedDict([('s!', OrderedDict([('c', 'c'), ('d', 'd')]))])
    >>> for c in _build_struct_from_tree(tree, sort = True): print(c)
    ARRAY(
      SELECT
        STRUCT(`c` as `c`, `d` as `d`)
      FROM UNNEST(s) as `_`
      ORDER BY `c`, `d`
    ) as `s`

    >>> tree = OrderedDict([('s', OrderedDict([('e!', '_')]))])
    >>> for c in _build_struct_from_tree(tree, sort = True): print(c)
    STRUCT(ARRAY(
      SELECT
        `_`
      FROM UNNEST(`s`.`e`) as `_`
      ORDER BY `_`
    ) as `e`) as `s`

    >>> tree = OrderedDict([('l1!', OrderedDict([('l2!', OrderedDict([('a', 'a'), ('b', 'b')]))]))])
    >>> for c in _build_struct_from_tree(tree, sort = True): print(c)
    ARRAY(
      SELECT
        STRUCT(ARRAY(
      SELECT
        STRUCT(`a` as `a`, `b` as `b`)
      FROM UNNEST(l2) as `_`
      ORDER BY `a`, `b`
    ) as `l2`)
      FROM UNNEST(l1) as `_`
      ORDER BY TO_JSON_STRING(ARRAY(
      SELECT
        STRUCT(`a` as `a`, `b` as `b`)
      FROM UNNEST(l2) as `_`
      ORDER BY `a`, `b`
    ))
    ) as `l1`

    >>> tree = OrderedDict([('l1!', OrderedDict([('s', OrderedDict([('a', 's.a'), ('b', 's.b')]))]))])
    >>> for c in _build_struct_from_tree(tree, sort = True): print(c)
    ARRAY(
      SELECT
        STRUCT(STRUCT(`s`.`a` as `a`, `s`.`b` as `b`) as `s`)
      FROM UNNEST(l1) as `_`
      ORDER BY TO_JSON_STRING(STRUCT(`s`.`a` as `a`, `s`.`b` as `b`))
    ) as `l1`

    :param node:
    :param sort: If set to true, will ensure that all arrays are canonically sorted
    :return:
    """

    def aux(node: OrderedTree, prefix: str = ""):
        def json_if_not_sortable(col: Column, is_sortable: bool) -> Column:
            if not is_sortable:
                return f.expr(f"TO_JSON_STRING({col.expr})")
            else:
                return col

        cols = []
        for key, col_or_children in node.items():
            is_repeated = key[-1] == REPETITION_MARKER
            is_struct = col_or_children is not None and not isinstance(col_or_children, (str, Column))
            is_sortable = not (is_repeated or is_struct)
            key_no_sep = key.replace(REPETITION_MARKER, "")
            if not is_struct:
                col = f.col(prefix + key_no_sep)
                transform_col = str_to_col(col_or_children)
                if is_repeated:
                    sort_cols = f.col("_") if sort else None
                    col = transform(col, transform_col, sort_cols)
                else:
                    col = transform_col
                cols.append((col.alias(key_no_sep), is_sortable))
            else:
                if is_repeated:
                    fields = aux(col_or_children, prefix="")
                    if sort:
                        sort_cols = [json_if_not_sortable(field, is_sortable) for field, is_sortable in fields]
                    else:
                        sort_cols = None
                    transform_col = f.struct(*[field for field, is_sortable in fields])
                    struct_col = transform(Column(prefix + key_no_sep), transform_col, sort_cols).alias(key_no_sep)
                else:
                    fields = aux(col_or_children, prefix=prefix + key + STRUCT_SEPARATOR)
                    fields = [field for field, is_array in fields]
                    struct_col = f.struct(*fields).alias(key_no_sep)
                cols.append((struct_col, is_sortable))
        return cols

    cols = aux(node)
    return [col for col, is_array in cols]


def _resolve_nested_columns(columns: Dict[str, StringOrColumn], sort: bool = False) -> List[Column]:
    """

    >>> _resolve_nested_columns({
    ...   "s!.c": f.col("c"),
    ...   "s!.d": f.col("d").cast("FLOAT64")
    ... })
    [Column('ARRAY(
      SELECT
        STRUCT(`c` as `c`, CAST(`d` as FLOAT64) as `d`)
      FROM UNNEST(s) as `_`
    )')]

    >>> _resolve_nested_columns({
    ...   "s!.e!": f.col("_").cast("FLOAT64"),
    ... })
    [Column('ARRAY(
      SELECT
        STRUCT(ARRAY(
      SELECT
        CAST(`_` as FLOAT64)
      FROM UNNEST(`e`) as `_`
    ) as `e`)
      FROM UNNEST(s) as `_`
    )')]

    >>> _resolve_nested_columns({
    ...   "s!.c": f.col("c"),
    ...   "s!.d": f.col("d"),
    ... }, sort = True)
    [Column('ARRAY(
      SELECT
        STRUCT(`c` as `c`, `d` as `d`)
      FROM UNNEST(s) as `_`
      ORDER BY `c`, `d`
    )')]

    >>> _resolve_nested_columns({
    ...   "s!.e!": f.col("_"),
    ... }, sort = True)
    [Column('ARRAY(
      SELECT
        STRUCT(ARRAY(
      SELECT
        `_`
      FROM UNNEST(`e`) as `_`
      ORDER BY `_`
    ) as `e`)
      FROM UNNEST(s) as `_`
      ORDER BY TO_JSON_STRING(ARRAY(
      SELECT
        `_`
      FROM UNNEST(`e`) as `_`
      ORDER BY `_`
    ))
    )')]

    :param columns:
    :param sort: If set to true, will ensure that all arrays are canonically sorted
    :return:
    """
    tree = _build_nested_struct_tree(columns)
    return _build_struct_from_tree(tree, sort)

# TODO: Transform into DataFrame.select_nested and add DataFrame.with_nested_columns
def _select_nested_columns(df: DataFrame, columns: Dict[str, StringOrColumn], sort: bool = False) -> DataFrame:
    """

    >>> bq = BigQueryBuilder(get_bq_client())
    >>> df = bq.sql('''
    ...  SELECT * FROM UNNEST([
    ...    STRUCT(1 as id, [STRUCT(1 as a, 2 as b), STRUCT(3 as a, 4 as b)] as s)
    ...  ])
    ... ''')
    >>> df.show()
    +----+--------------------------------------+
    | id |                                    s |
    +----+--------------------------------------+
    |  1 | [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}] |
    +----+--------------------------------------+
    >>> _select_nested_columns(df, {
    ...   "s!.b": f.col("b").cast("FLOAT64")
    ... }).show()
    +--------------------------+
    |                        s |
    +--------------------------+
    | [{'b': 2.0}, {'b': 4.0}] |
    +--------------------------+

    >>> df = bq.sql('''
    ...  SELECT * FROM UNNEST([
    ...    STRUCT(1 as id, [STRUCT(1 as a, 1 as b), STRUCT(1 as a, 2 as b)] as s),
    ...    STRUCT(2 as id, [STRUCT(1 as a, 2 as b), STRUCT(1 as a, 1 as b)] as s)
    ...  ])
    ... ''')
    >>> df.show()
    +----+--------------------------------------+
    | id |                                    s |
    +----+--------------------------------------+
    |  1 | [{'a': 1, 'b': 1}, {'a': 1, 'b': 2}] |
    |  2 | [{'a': 1, 'b': 2}, {'a': 1, 'b': 1}] |
    +----+--------------------------------------+
    >>> _select_nested_columns(df, {
    ...   "s!.a": "a",
    ...   "s!.b": "b"
    ... }, sort=True).show()
    +--------------------------------------+
    |                                    s |
    +--------------------------------------+
    | [{'a': 1, 'b': 1}, {'a': 1, 'b': 2}] |
    | [{'a': 1, 'b': 1}, {'a': 1, 'b': 2}] |
    +--------------------------------------+

    >>> df = bq.sql('''
    ...  SELECT * FROM UNNEST([
    ...    STRUCT(1 as id, [STRUCT([1, 2, 3] as e)] as s)
    ...  ])
    ... ''')
    >>> df.show()
    +----+--------------------+
    | id |                  s |
    +----+--------------------+
    |  1 | [{'e': [1, 2, 3]}] |
    +----+--------------------+
    >>> _select_nested_columns(df, {
    ...   "s!.e!": f.col("_").cast("FLOAT64"),
    ... }).show()
    +--------------------------+
    |                        s |
    +--------------------------+
    | [{'e': [1.0, 2.0, 3.0]}] |
    +--------------------------+

    >>> df = bq.sql('''
    ...  SELECT * FROM UNNEST([
    ...    STRUCT(1 as id, [STRUCT([1, 2, 3] as e)] as s),
    ...    STRUCT(2 as id, [STRUCT([3, 2, 1] as e)] as s)
    ...  ])
    ... ''')
    >>> df.show()
    +----+--------------------+
    | id |                  s |
    +----+--------------------+
    |  1 | [{'e': [1, 2, 3]}] |
    |  2 | [{'e': [3, 2, 1]}] |
    +----+--------------------+
    >>> _select_nested_columns(df, {
    ...   "s!.e!": f.col("_"),
    ... }, sort = True).show()
    +--------------------+
    |                  s |
    +--------------------+
    | [{'e': [1, 2, 3]}] |
    | [{'e': [1, 2, 3]}] |
    +--------------------+

    :param columns:
    :param sort: If set to true, will ensure that all arrays are canonically sorted
    :return:
    """
    return df.select(*_resolve_nested_columns(columns, sort))


def canonize_arrays(df: DataFrame) -> DataFrame:
    """Given a DataFrame, sort all columns of type arrays (even nested ones) in a canonical order,
    making them comparable

    >>> bq = BigQueryBuilder(get_bq_client())
    >>> df = bq.sql('SELECT [3, 2, 1] as a')
    >>> df.show()
    +-----------+
    |         a |
    +-----------+
    | [3, 2, 1] |
    +-----------+
    >>> canonize_arrays(df).show()
    +-----------+
    |         a |
    +-----------+
    | [1, 2, 3] |
    +-----------+

    >>> df = bq.sql('SELECT [STRUCT(2 as a, 1 as b), STRUCT(1 as a, 2 as b), STRUCT(1 as a, 1 as b)] as s')
    >>> df.show()
    +--------------------------------------------------------+
    |                                                      s |
    +--------------------------------------------------------+
    | [{'a': 2, 'b': 1}, {'a': 1, 'b': 2}, {'a': 1, 'b': 1}] |
    +--------------------------------------------------------+
    >>> canonize_arrays(df).show()
    +--------------------------------------------------------+
    |                                                      s |
    +--------------------------------------------------------+
    | [{'a': 1, 'b': 1}, {'a': 1, 'b': 2}, {'a': 2, 'b': 1}] |
    +--------------------------------------------------------+

    >>> df = bq.sql('''SELECT [
    ...         STRUCT([STRUCT(2 as a, 2 as b), STRUCT(2 as a, 1 as b)] as l2),
    ...         STRUCT([STRUCT(1 as a, 2 as b), STRUCT(1 as a, 1 as b)] as l2)
    ...     ] as l1
    ... ''')
    >>> df.show()
    +----------------------------------------------------------------------------------------------+
    |                                                                                           l1 |
    +----------------------------------------------------------------------------------------------+
    | [{'l2': [{'a': 2, 'b': 2}, {'a': 2, 'b': 1}]}, {'l2': [{'a': 1, 'b': 2}, {'a': 1, 'b': 1}]}] |
    +----------------------------------------------------------------------------------------------+
    >>> canonize_arrays(df).show()
    +----------------------------------------------------------------------------------------------+
    |                                                                                           l1 |
    +----------------------------------------------------------------------------------------------+
    | [{'l2': [{'a': 1, 'b': 1}, {'a': 1, 'b': 2}]}, {'l2': [{'a': 2, 'b': 1}, {'a': 2, 'b': 2}]}] |
    +----------------------------------------------------------------------------------------------+

    >>> df = bq.sql('''SELECT [
    ...         STRUCT(STRUCT(2 as a, 2 as b) as s),
    ...         STRUCT(STRUCT(1 as a, 2 as b) as s)
    ...     ] as l1
    ... ''')
    >>> df.show()
    +----------------------------------------------------+
    |                                                 l1 |
    +----------------------------------------------------+
    | [{'s': {'a': 2, 'b': 2}}, {'s': {'a': 1, 'b': 2}}] |
    +----------------------------------------------------+
    >>> canonize_arrays(df).show()
    +----------------------------------------------------+
    |                                                 l1 |
    +----------------------------------------------------+
    | [{'s': {'a': 1, 'b': 2}}, {'s': {'a': 2, 'b': 2}}] |
    +----------------------------------------------------+

    :return:
    """
    schema_flat = flatten_schema(
        df.schema, explode=True, struct_separator=STRUCT_SEPARATOR, array_separator=REPETITION_MARKER
    )

    def get_col_short_name(col: str):
        if col[-1] == REPETITION_MARKER:
            return ELEMENT_COL_NAME
        else:
            return col.split(REPETITION_MARKER + STRUCT_SEPARATOR)[-1]

    columns = {field.name: get_col_short_name(field.name) for field in schema_flat}
    return _select_nested_columns(df, columns, sort=True)
