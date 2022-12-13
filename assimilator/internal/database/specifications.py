from assimilator.core.database import Specification


class DictSpecification(Specification):
    def apply(self, query: str) -> str:     # returns the key
        return super(DictSpecification, self).apply(query)


class DictKeySpecification(DictSpecification):
    def __init__(self, key: str):
        self.key = key

    def apply(self, query):
        return f"{query}{self.key}"
