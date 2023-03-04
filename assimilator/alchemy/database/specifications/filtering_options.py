from typing import Callable, Any

from sqlalchemy import column
from sqlalchemy.sql.elements import ColumnClause

from assimilator.core.database.specifications.filtering_options import \
    FilteringOptions, FILTERING_OPTIONS_SEPARATOR


class AlchemyFilteringOptions(FilteringOptions):
    table_name: str = None

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

        return super(AlchemyFilteringOptions, self).parse_field(raw_field=raw_field, value=value)

    @staticmethod
    def _eq(field, value):
        return AlchemyFilteringOptions._convert_field(field) == value

    @staticmethod
    def _gt(field, value):
        return AlchemyFilteringOptions._convert_field(field) > value

    @staticmethod
    def _gte(field, value):
        return AlchemyFilteringOptions._convert_field(field) >= value

    @staticmethod
    def _lt(field, value):
        return AlchemyFilteringOptions._convert_field(field) < value

    @staticmethod
    def _lte(field, value):
        return AlchemyFilteringOptions._convert_field(field) <= value

    @staticmethod
    def _not(field, value):
        return AlchemyFilteringOptions._convert_field(field) != value

    @staticmethod
    def _is(field, value):
        return AlchemyFilteringOptions._convert_field(field).is_(value)

    @staticmethod
    def _like(field, value):
        return AlchemyFilteringOptions._convert_field(field).like(value)

    @staticmethod
    def _regex(field, value):
        return AlchemyFilteringOptions._convert_field(field).regexp_match(value)


__all__ = [
    'AlchemyFilteringOptions',
]
