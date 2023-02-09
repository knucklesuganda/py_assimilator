from sqlalchemy import column
from sqlalchemy.sql.elements import ColumnClause

from assimilator.core.database.specifications.filtering_options import FilteringOptions


class AlchemyFilteringOptions(FilteringOptions):
    def _convert_field(self, field: str) -> ColumnClause:
        return column(field, is_literal=True)

    def _eq(self, field, value):
        return self._convert_field(field) == value

    def _gt(self, field, value):
        return self._convert_field(field) > value

    def _gte(self, field, value):
        return self._convert_field(field) >= value

    def _lt(self, field, value):
        return self._convert_field(field) < value

    def _lte(self, field, value):
        return self._convert_field(field) <= value

    def _not(self, field, value):
        return self._convert_field(field) != value

    def _is(self, field, value):
        return self._convert_field(field).is_(value)

    def _like(self, field, value):
        return self._convert_field(field).like(value)

    def _regex(self, field, value):
        return self._convert_field(field).regexp_match(value)


__all__ = [
    'AlchemyFilteringOptions',
]
