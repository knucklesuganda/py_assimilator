from assimilator.core.database import Specification


class DictSpecification(Specification):
    def apply(self, query: str) -> str:     # returns the key
        return super(DictSpecification, self).apply(query)


class DictKeySpecification(DictSpecification):
    def __init__(self, id: str):
        self.id = id

    def apply(self, query):
        return f"{query}{self.id}"
