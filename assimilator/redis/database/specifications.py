from assimilator.core.database import Specification


class RedisSpecification(Specification):
    def apply(self, query: str) -> str:
        return super(RedisSpecification, self).apply(query)


class FilterSpecification(RedisSpecification):
    def __init__(self, filters):
        self.filters = filters

    def apply(self, query: str) -> str:
        return f"{query}{self.filters}"
