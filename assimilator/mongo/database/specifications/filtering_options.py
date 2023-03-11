from assimilator.core.database.specifications.filtering_options import\
    FilteringOptions, FILTERING_OPTIONS_SEPARATOR


class MongoFilteringOptions(FilteringOptions):
    @staticmethod
    def _convert_field(field: str) -> str:
        return field.replace(FILTERING_OPTIONS_SEPARATOR, ".")

    def _eq(self, field: str, value):
        return {self._convert_field(field): {"$eq": value}}

    def _gt(self, field: str, value):
        return {self._convert_field(field): {"$gt": value}}

    def _gte(self, field: str, value):
        return {self._convert_field(field): {"$gte": value}}

    def _lt(self, field: str, value):
        return {self._convert_field(field): {"$lt": value}}

    def _lte(self, field: str, value):
        return {self._convert_field(field): {"$lte": value}}

    def _not(self, field: str, value):
        return {self._convert_field(field): {"$ne": value}}

    def _is(self, field: str, value):
        return self._eq(self._convert_field(field), value)

    def _like(self, field: str, value):
        return self._regex(field, f'^{value.replace("%", ".*?")}$')

    def _regex(self, field: str, value):
        return {self._convert_field(field): {"$regex": value}}


__all__ = [
    'MongoFilteringOptions',
]
