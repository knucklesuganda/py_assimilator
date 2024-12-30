from typing import Any, Callable

from sqlalchemy import column
from sqlalchemy.sql.elements import ColumnClause

from assimilator.core.database.specifications.filtering_options import (
    FILTERING_OPTIONS_SEPARATOR,
    FilteringOptions,
)


class AlchemyFilteringOptions(FilteringOptions):
    table_name: str | None = None

    @staticmethod
    def _convert_field(field: str) -> ColumnClause:
        field_parts = field.split(FILTERING_OPTIONS_SEPARATOR)

        if len(field_parts) > 2:
            field = ".".join(field_parts[-2:])
        else:
            field = ".".join(field_parts)

        return column(field, is_literal=True)

    def parse_field(self, raw_field: str, value: Any) -> Callable:
        fields = raw_field.split(FILTERING_OPTIONS_SEPARATOR)
        last_field = fields[-1]

        if len(fields) == 1 and self.table_name is not None:
            last_field = f"{self.table_name}.{last_field}"
            filter_func = self.filter_options.get(last_field, self.get_default_filter())
            return filter_func(last_field, value)

        return super().parse_field(raw_field=raw_field, value=value)

    def _eq(self, field, value):
        return AlchemyFilteringOptions._convert_field(field) == value

    def _gt(self, field, value):
        return AlchemyFilteringOptions._convert_field(field) > value

    def _gte(self, field, value):
        return AlchemyFilteringOptions._convert_field(field) >= value

    def _lt(self, field, value):
        return AlchemyFilteringOptions._convert_field(field) < value

    def _lte(self, field, value):
        return AlchemyFilteringOptions._convert_field(field) <= value

    def _not(self, field, value):
        return AlchemyFilteringOptions._convert_field(field) != value

    def _is(self, field, value):
        return AlchemyFilteringOptions._convert_field(field).is_(value)

    def _like(self, field, value):
        return AlchemyFilteringOptions._convert_field(field).like(value)

    def _regex(self, field, value):
        return AlchemyFilteringOptions._convert_field(field).regexp_match(value)


__all__ = [
    "AlchemyFilteringOptions",
]
