from functools import wraps
from abc import ABC
from typing import Callable, TypeVar, Type, Any, Union

from assimilator.core.database.specifications.filtering_options import FilteringOptions
from assimilator.core.database.specifications.types import (
    OrderSpecificationProtocol,
    PaginateSpecificationProtocol,
    OnlySpecificationProtocol,
    JoinSpecificationProtocol,
)

QueryT = TypeVar("QueryT")


class Specification(ABC):
    def __call__(self, query: QueryT, **context: Any) -> QueryT:
        raise NotImplementedError("Specification must specify __call__()")


class FilterSpecification(Specification, ABC):
    filtering_options_cls: Type[FilteringOptions]

    def __init__(self, *filters, **named_filters):
        self.filters = list(filters)
        self.filtering_options = self.filtering_options_cls()

        for field, value in named_filters.items():
            self.filters.append(
                self.filtering_options.parse_field(raw_field=field, value=value)
            )

    def __or__(self, other: 'SpecificationType') -> 'FilterSpecification':
        raise NotImplementedError("or() is not implemented for FilterSpecification")

    def __and__(self, other: 'SpecificationType') -> 'FilterSpecification':
        raise NotImplementedError("and() is not implemented for FilterSpecification")

    def __invert__(self):
        raise NotImplementedError("invert() is not implemented for FilterSpecification")

    def __str__(self):
        return f'filter_spec({self.filters})'


def specification(func: Callable) -> Callable:
    def create_specification(*args, **kwargs):

        @wraps(func)
        def created_specification(query: QueryT, **context) -> QueryT:
            return func(*args, **kwargs, query=query, **context)

        created_specification: func
        return created_specification

    return create_specification


class SpecificationList:
    filter: Type[FilterSpecification]
    order: OrderSpecificationProtocol
    paginate: PaginateSpecificationProtocol
    join: JoinSpecificationProtocol
    only: OnlySpecificationProtocol


SpecificationType = Union[Callable, Specification]


__all__ = [
    'SpecificationList',
    'Specification',
    'specification',
    'SpecificationType',
    'FilterSpecification',
]
