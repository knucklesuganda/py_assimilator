from sqlalchemy import column
from sqlalchemy.sql.elements import ColumnClause

from assimilator.core.database.specifications.filtering_options import \
    FilteringOptions, FILTERING_OPTIONS_SEPARATOR


class AlchemyFilteringOptions(FilteringOptions):
    @staticmethod
    def _convert_field(field: str) -> ColumnClause:
        field_parts = field.split(FILTERING_OPTIONS_SEPARATOR)

        if len(field_parts) > 2:
            field = ".".join(field_parts[-2:])
        else:
            field = ".".join(field_parts)

        return column(field, is_literal=True)

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
