"""
Copyright 2021 Objectiv B.V.
"""
import re
from typing import Union, TYPE_CHECKING, Optional, Pattern

from sqlalchemy.engine import Dialect

from bach.partitioning import get_order_by_expression
from bach.series import Series
from bach.expression import Expression, AggregateFunctionExpression, get_variable_tokens
from bach.series.series import WrappedPartition
from bach.types import StructuredDtype
from sql_models.constants import DBDialect
from sql_models.util import DatabaseNotSupportedException, is_bigquery, is_postgres

if TYPE_CHECKING:
    from bach.series import SeriesBoolean
    from bach import DataFrame, SortColumn, SeriesJson


class StringOperation:

    def __init__(self, base: 'SeriesString'):
        self._base = base

    def __getitem__(self, start: Union[int, slice]) -> 'SeriesString':
        """
        Get a python string slice using DB functions. Format follows standard slice format
        Note: this is called 'slice' to not destroy index selection logic
        :param item: an int for a single character, or a slice for some nice slicing
        :return: SeriesString with the slice applied
        """
        if isinstance(start, (int, type(None))):
            item = slice(start, start + 1)
        elif isinstance(start, slice):
            item = start
        else:
            raise ValueError(f'Type not supported {type(start)}')

        expression = self._base.expression

        if item.start is not None and item.start < 0:
            expression = Expression.construct(f'right({{}}, {abs(item.start)})', expression)
            if item.stop is not None:
                if item.stop <= 0 and item.stop > item.start:
                    # we needed to check stop <= 0, because that would mean we're going the wrong direction
                    # and that's not supported
                    expression = Expression.construct(f'left({{}}, {item.stop - item.start})', expression)
                else:
                    expression = Expression.construct("''")

        elif item.stop is not None and item.stop < 0:
            # we need to get the full string, minus abs(stop) chars with possibly item.start as an offset
            offset = 1 if item.start is None else item.start + 1
            length_offset = item.stop - (offset - 1)
            expression = Expression.construct(
                f'substr({{}}, {offset}, greatest(0, length({{}}){length_offset}))',
                expression, expression
            )

        else:
            # positives only
            if item.stop is None:
                if item.start is None:
                    # full string, what are we doing here?
                    # current expression is okay.
                    pass
                else:
                    # full string starting at start
                    expression = Expression.construct(f'substr({{}}, {item.start + 1})', expression)
            else:
                if item.start is None:
                    expression = Expression.construct(f'left({{}}, {item.stop})', expression)
                else:
                    if item.stop > item.start:
                        expression = Expression.construct(
                            f'substr({{}}, {item.start + 1}, {item.stop - item.start})',
                            expression
                        )
                    else:
                        expression = Expression.construct("''")

        return self._base.copy_override(expression=expression)

    def slice(self, start=None, stop=None) -> 'SeriesString':
        """
        slice a string like you would in Python, either by calling this method, or by slicing directly
        on the `str` accessor.

        .. code-block:: python

            a.str[3]            # get one char
            a.str[3:5]          # get a slice from char 3-5
            a.str.slice(3, 5)   # idem
        """
        if isinstance(start, slice):
            return self.__getitem__(start)
        return self.__getitem__(slice(start, stop))

    def replace(
        self,
        pat: Union[str, Pattern],
        repl: str,
        n: int = -1,
        case: bool = None,
        flags: int = 0,
        regex: bool = False,
    ) -> 'SeriesString':
        """
        replace each occurrence of a pattern in SeriesString.

        :param pat: string or compiled pattern to use for replacement.
        :param repl: string to use as a replacement for each occurrence
        :param n: number of occurrences to be replaced. Only n=-1 is supported (all occurrences)
        :param case: determines if the replace is case insensitive. Considered only when regex=True.
        :param flags: regex module flags. Considered only when regex=True.
        :param regex: Determines if provided pattern is a regular expression or not.

        .. note::
          Replacements based on regular expressions are not supported yet. Therefore:
              - `pat` parameter must be string type
              - `case`, `flags`, `regex` will not be considered on replacement
        """
        if isinstance(pat, re.Pattern) or regex:
            raise NotImplementedError('Regex patterns are not supported yet.')

        if n != -1:
            raise NotImplementedError('Replacement for all occurrences is supported only.')

        expr = Expression.construct(
            f'REPLACE({{}}, {{}}, {{}})',
            self._base,
            Expression.string_value(pat),
            Expression.string_value(repl),
        )
        return self._base.copy_override(expression=expr)

    def upper(self) -> 'SeriesString':
        """
        converts string values into uppercase.

        :return: SeriesString with all alphabetic characters in uppercase
        """
        return self._base.copy_override(
            expression=Expression.construct('upper({})', self._base)
        )

    def lower(self) -> 'SeriesString':
        """
        converts string values into lowercase.

        :return: SeriesString with all alphabetic characters in lowercase
        """
        return self._base.copy_override(
            expression=Expression.construct('lower({})', self._base)
        )


class SeriesString(Series):
    """
    A Series that represents the string type and its specific operations

    **Operations**

    Strings can be concatenated using the '+' operator, and the 'str' accessor can be used to get access
    to slices.

    Example:

    .. code-block:: python

        c = a + b  # concat the strings.
        a.str[3]   # get one char
        a.str[3:5] # get a slice from char 3-5


    **Database support and types**

    * Postgres: utilizes the 'text' database type.
    * Athena: utilizes the 'varchar' database type.
    * BigQuery: utilizes the 'STRING' database type.
    """

    dtype = 'string'
    dtype_aliases = ('text', str)
    supported_db_dtype = {
        DBDialect.POSTGRES: 'text',
        DBDialect.ATHENA: 'varchar',
        DBDialect.BIGQUERY: 'STRING'
    }
    supported_value_types = (str, type(None))  # NoneType ends up as a string for now

    @classmethod
    def supported_literal_to_expression(cls, dialect: Dialect, literal: Expression) -> Expression:
        # We override the parent class here because strings are really common, and we don't strictly need
        # to cast them. As all supported databases will interpret a string literal as a string.
        # Not casting string literals greatly improves the readability of the generated SQL.

        # However, there is an edge case: NULL values should be cast to string. e.g. BigQuery considers a
        # naked NULL to be INT64. Additionally, we'll always cast variables, just so this keeps working if
        # the variable get set to `None`
        if literal.to_sql(dialect=dialect).upper() == 'NULL' or get_variable_tokens([literal]):
            return super().supported_literal_to_expression(dialect=dialect, literal=literal)
        return literal

    @classmethod
    def supported_value_to_literal(
        cls,
        dialect: Dialect,
        value: str,
        dtype: StructuredDtype
    ) -> Expression:
        return Expression.string_value(value)

    @classmethod
    def dtype_to_expression(cls, dialect: Dialect, source_dtype: str, expression: Expression) -> Expression:
        if source_dtype == 'string':
            return expression
        return Expression.construct(f'cast({{}} as {cls.get_db_dtype(dialect)})', expression)

    def get_dummies(
        self,
        prefix: Optional[str] = None,
        prefix_sep: str = '_',
        dummy_na: bool = False,
        dtype: str = 'int64',
    ) -> 'DataFrame':
        """
        Convert each unique category/value from the series into a dummy/indicator variable.

        :param prefix: String to append to each new column name. By default, the prefix will be the name of
            the caller.
        :param prefix_sep: Separated between the prefix and label.
        :param dummy_na: If true, it will include ``nan`` as a variable.
        :param dtype: dtype of all new columns

        :return: DataFrame

        .. note::
            Series should contain at least one index level.
        """
        return self.to_frame().get_dummies(
            prefix=prefix, prefix_sep=prefix_sep, dummy_na=dummy_na, dtype=dtype,
        )

    @property
    def str(self) -> StringOperation:
        """
        Get access to string operations.

        .. autoclass:: bach.series.series_string.StringOperation
            :members:

        """
        return StringOperation(self)

    def __add__(self, other) -> 'Series':
        return self._binary_operation(other, 'concat', '{} || {}', other_dtypes=('string',))

    def _comparator_operation(self, other, comparator, other_dtypes=tuple(['string']),
                              strict_other_dtypes=tuple()) -> 'SeriesBoolean':
        return super()._comparator_operation(other, comparator, other_dtypes, strict_other_dtypes)

    def to_json_array(self, partition: Optional[WrappedPartition] = None) -> 'SeriesJson':
        """
        Aggregate function: Group the values of this Series into a json array

        The order of the values in the array will be based of the order of the values in this Series. If
        this Series does not have a deterministic sorting, then the values are additionally sorted by the
        values themselves. Null values will always be sorted last when aggregating all values, following
        default sorting behavior for DataFrame/Series.

        :param partition: The partition to apply, optional.
        :return: SeriesJson containing an array of strings on each row.
        """
        order_by = self.order_by
        # Add this series as the final column to sort on. If the order_by is deterministic then this won't
        # change the sorting. If order_by was not deterministic, then this will make it deterministic.
        from bach import SortColumn
        order_by += [SortColumn(expression=self.expression, asc=True)]

        order_by_expr = get_order_by_expression(
            dialect=self.engine.dialect, order_by=order_by, na_position='last',
        )
        array_agg_expression = AggregateFunctionExpression.construct('array_agg({} {})', self, order_by_expr)
        if is_postgres(self.engine):
            expression = Expression.construct('to_jsonb({})', array_agg_expression)
        elif is_bigquery(self.engine):
            expression = Expression.construct('to_json_string({})', array_agg_expression)
        else:
            raise DatabaseNotSupportedException(self.engine)

        result = self._derived_agg_func(partition, expression)
        from bach import SeriesJson
        return result.copy_override_type(SeriesJson)
