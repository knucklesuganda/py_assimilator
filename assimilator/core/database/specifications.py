from abc import ABC, abstractmethod
from functools import wraps


class Specification(ABC):
    @abstractmethod
    def apply(self, query):
        raise NotImplementedError("Specification must specify apply()")

    def __call__(self, query):
        return self.apply(query)


def specification(func: callable, *args, **kwargs):
    @wraps(func)
    def specification_wrapper(query):
        return func(query, *args, **kwargs)

    return specification_wrapper
