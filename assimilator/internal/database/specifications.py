from assimilator.core.database import Specification, specification


class InternalSpecification(Specification):
    def apply(self, query: str) -> str:     # returns the str key
        return super(InternalSpecification, self).apply(query)


@specification
def key_specification(query, key: str):
    return f"{query}{key}"
