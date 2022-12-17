from assimilator.core.database import Specification, specification, SpecificationList


class InternalSpecification(Specification):
    def apply(self, query: str) -> str:     # returns the str key
        return super(InternalSpecification, self).apply(query)


@specification
def internal_filter(query: str, key: str) -> str:
    return f"{query}{key}"


@specification
def internal_order(query: str) -> str:
    return query


@specification
def internal_paginate(query: str) -> str:
    return query


@specification
def internal_join(query: str) -> str:
    return query


class InternalSpecificationList(SpecificationList):
    filter = internal_filter
    order = internal_order
    paginate = internal_paginate
    join = internal_join


__all__ = [
    'InternalSpecification',
    'internal_filter',
    'internal_order',
    'internal_paginate',
    'internal_join',
    'InternalSpecificationList',
]
