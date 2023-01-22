from assimilator.core.database.specifications.filtering_options import FilteringOptions


class MongoFilteringOptions(FilteringOptions):
    def _eq(self, field: str, value):
        return {field: {"$eq": value}}

    def _gt(self, field: str, value):
        return {field: {"$gt": value}}

    def _gte(self, field: str, value):
        return {field: {"$gte": value}}

    def _lt(self, field: str, value):
        return {field: {"$lt": value}}

    def _lte(self, field: str, value):
        return {field: {"$lte": value}}

    def _not(self, field: str, value):
        return {field: {"$ne": value}}

    def _is(self, field: str, value):
        return self._eq(field, value)

    def _like(self, field: str, value):
        return self._regex(field, f'^{value.replace("%", ".*?")}$')

    def _regex(self, field: str, value):
        return {field: {"$regex": value}}


__all__ = [
    'MongoFilteringOptions',
]
