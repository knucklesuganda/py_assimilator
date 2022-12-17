from abc import ABC, abstractmethod
from typing import Callable

from makefun import wraps


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
            return func(*args, query=query, **kwargs)

        return created_specification
    return create_specification


class SpecificationList:
    filter: Specification
    order: Specification
    paginate: Specification
    join: Specification


__all__ = [
    'SpecificationList',
    'Specification',
    'specification',
]
