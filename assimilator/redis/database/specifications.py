from assimilator.core.database import Specification


class RedisSpecification(Specification):
    def apply(self, query: str) -> str:
        return super(RedisSpecification, self).apply(query)


class RedisKeySpecification(RedisSpecification):
    def __init__(self, key: str):
        self.filters = key

    def apply(self, query: str) -> str:
        return f"{query}{self.filters}"
