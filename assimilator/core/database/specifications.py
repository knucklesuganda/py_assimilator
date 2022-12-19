from abc import ABC, abstractmethod
from typing import Callable, Union
from functools import wraps


class Specification(ABC):
    @abstractmethod
    def apply(self, query):
        raise NotImplementedError("Specification must specify apply()")

    def __call__(self, query):
        return self.apply(query)


def specification(func: Callable):
    def create_specification(*args, **kwargs):

        @wraps(func)
        def created_specification(query):
            return func(*args, **kwargs, query=query)

        return created_specification
    return create_specification


SpecificationType = Union[Specification, Callable]


class SpecificationList:
    filter: SpecificationType
    order: SpecificationType
    paginate: SpecificationType
    join: SpecificationType


__all__ = [
    'SpecificationList',
    'Specification',
    'specification',
    'SpecificationType',
]
