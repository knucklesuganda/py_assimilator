from typing import List

from assimilator.core.database import Specification, specification, SpecificationList
from assimilator.internal.database.models import InternalModel


class InternalSpecification(Specification):
    def apply(self, query: str) -> str:     # returns the str key
        return super(InternalSpecification, self).apply(query)


@specification
def internal_filter(*args, query: str, **kwargs) -> str:
    return f'{query}{"".join(*args)}'


@specification
def internal_order(*args, query: List[InternalModel], **kwargs) -> List[InternalModel]:
    return sorted(
        query,
        key=lambda item: [getattr(item, argument) for argument in (args, *kwargs.keys())],
    )


@specification
def internal_paginate(limit: int, offset: int, query: List[InternalModel]) -> List[InternalModel]:
    return query[limit:offset]


@specification
def internal_join(*args, query: str, **kwargs) -> str:
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
