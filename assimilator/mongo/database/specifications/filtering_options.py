from typing import Any, Tuple

from bson import ObjectId

from assimilator.core.database.specifications.filtering_options import\
    FilteringOptions, FILTERING_OPTIONS_SEPARATOR
from assimilator.mongo.database.specifications.utils import rename_mongo_id, contains_mongo_id


class MongoFilteringOptions(FilteringOptions):
    @staticmethod
    def _convert_option(field: str, value: Any) -> Tuple[str, Any]:
        field = rename_mongo_id(field.replace(FILTERING_OPTIONS_SEPARATOR, "."))
        if contains_mongo_id(field):
            value = ObjectId(value)

        return field, value

    def _eq(self, field: str, value):
        field, value = self._convert_option(field=field, value=value)
        return {field: {"$eq": value}}

    def _gt(self, field: str, value):
        field, value = self._convert_option(field=field, value=value)
        return {field: {"$gt": value}}

    def _gte(self, field: str, value):
        field, value = self._convert_option(field=field, value=value)
        return {field: {"$gte": value}}

    def _lt(self, field: str, value):
        field, value = self._convert_option(field=field, value=value)
        return {field: {"$lt": value}}

    def _lte(self, field: str, value):
        field, value = self._convert_option(field=field, value=value)
        return {field: {"$lte": value}}

    def _not(self, field: str, value):
        field, value = self._convert_option(field=field, value=value)
        return {field: {"$ne": value}}

    def _is(self, field: str, value):
        field, value = self._convert_option(field=field, value=value)
        return self._eq(field, value)

    def _like(self, field: str, value):
        return self._regex(field, f'^{value.replace("%", ".*?")}$')

    def _regex(self, field: str, value):
        field, value = self._convert_option(field=field, value=value)
        return {field: {"$regex": value}}


__all__ = [
    'MongoFilteringOptions',
]
