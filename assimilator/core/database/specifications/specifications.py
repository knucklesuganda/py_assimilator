from functools import wraps
from abc import ABC, abstractmethod
from typing import Callable, Union, TypeVar, Any, Type, final

from assimilator.core.database.specifications.filtering_options import FilteringOptions


QueryT = TypeVar("QueryT")


class Specification(ABC):
    @abstractmethod
    def apply(self, query: QueryT) -> QueryT:
        raise NotImplementedError("Specification must specify apply()")

    @final
    def __call__(self, query: QueryT) -> QueryT:
        return self.apply(query)


class FilterSpecification(Specification, ABC):
    filtering_options_cls: Type[FilteringOptions]

    def __init__(self, *filters, **named_filters):
        self.filters = list(filters)
        self.filtering_options = self.filtering_options_cls()

        for field, value in named_filters.items():
            option, filter_func = self.filtering_options.parse_filter(raw_filter=field)
            self.filter_parsed(filter_func=filter_func, field=field.replace(option, ""), value=value)

    def filter_parsed(self, filter_func: Callable, field: str, value: Any):
        raise NotImplementedError("filter_parsed() is not implemented")

    def __or__(self, other: 'FilterSpecification') -> 'FilterSpecification':
        raise NotImplementedError("or() is not implemented for FilterSpecification")

    def __and__(self, other: 'FilterSpecification') -> 'FilterSpecification':
        raise NotImplementedError("and() is not implemented for FilterSpecification")

    def __invert__(self):
        raise NotImplementedError("invert() is not implemented for FilterSpecification")

    def __str__(self):
        return f'{type(self.__class__).__name__}({self.filters})'


def specification(func: Callable) -> Callable[[Any], QueryT]:
    def create_specification(*args, **kwargs):
        @wraps(func)
        def created_specification(query: QueryT) -> QueryT:
            return func(*args, **kwargs, query=query)

        return created_specification

    return create_specification


SpecificationType = Union[Type[Specification], Callable]


class SpecificationList:
    filter: Type[FilterSpecification]
    order: Union[Specification, Callable]
    paginate: SpecificationType
    join: SpecificationType
    only: SpecificationType


__all__ = [
    'SpecificationList',
    'Specification',
    'specification',
    'SpecificationType',
    'FilterSpecification',
]
