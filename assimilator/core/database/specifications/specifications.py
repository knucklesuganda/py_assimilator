from functools import wraps
from abc import ABC, abstractmethod
from typing import Callable, Union, TypeVar, Type, final, Any

from assimilator.core.database.specifications.filtering_options import FilteringOptions
from assimilator.core.database.specifications.types import (
    OrderSpecificationProtocol,
    PaginateSpecificationProtocol,
    OnlySpecificationProtocol,
    JoinSpecificationProtocol,
)

QueryT = TypeVar("QueryT")


class Specification(ABC):
    @abstractmethod
    def apply(self, query: QueryT, **context: Any) -> QueryT:
        raise NotImplementedError("Specification must specify apply()")

    @final
    def __call__(self, query: QueryT, **context: Any) -> QueryT:
        return self.apply(query, **context)


class FilterSpecification(Specification, ABC):
    filtering_options_cls: Type[FilteringOptions]

    def __init__(self, *filters, **named_filters):
        self.filters = list(filters)
        self.filtering_options = self.filtering_options_cls()

        for field, value in named_filters.items():
            self.filters.append(
                self.filtering_options.parse_field(raw_field=field, value=value)
            )

    def __or__(self, other: 'FilterSpecification') -> 'FilterSpecification':
        raise NotImplementedError("or() is not implemented for FilterSpecification")

    def __and__(self, other: 'FilterSpecification') -> 'FilterSpecification':
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


SpecificationType = Union[Type[Specification], Callable]


class SpecificationList:
    filter: Type[FilterSpecification]
    order: OrderSpecificationProtocol
    paginate: PaginateSpecificationProtocol
    join: JoinSpecificationProtocol
    only: OnlySpecificationProtocol


__all__ = [
    'SpecificationList',
    'Specification',
    'specification',
    'SpecificationType',
    'FilterSpecification',
]
