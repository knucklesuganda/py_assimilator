from abc import ABC, abstractmethod
from typing import Callable, Union, TypeVar, Dict, Any, Tuple, Optional
from functools import wraps


QueryT = TypeVar("QueryT")


class Specification(ABC):
    @abstractmethod
    def apply(self, query: QueryT) -> QueryT:
        raise NotImplementedError("Specification must specify apply()")

    def __call__(self, query: QueryT) -> QueryT:
        return self.apply(query)


def filter_parameter_parser(
    field: str,
    value: Any,
    filter_mappings: Dict[str, Callable],
) -> Tuple[Optional[str], Optional[Any]]:
    for filter_ending, filter_func in filter_mappings.items():
        if field.endswith(filter_ending):
            return filter_ending, filter_func(field.replace(filter_ending, ""), value)

    return None, None


def specification(func: Callable):
    def create_specification(*args, **kwargs):

        @wraps(func)
        def created_specification(query: QueryT) -> QueryT:
            return func(*args, **kwargs, query=query)

        return created_specification

    return create_specification


SpecificationType = Union[Specification, Callable]


class SpecificationList:
    filter: SpecificationType
    order: SpecificationType
    paginate: SpecificationType
    join: SpecificationType
    only: SpecificationType


__all__ = [
    'SpecificationList',
    'Specification',
    'specification',
    'SpecificationType',
    'filter_parameter_parser',
]
