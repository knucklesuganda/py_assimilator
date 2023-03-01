from abc import ABC, abstractmethod
from typing import Optional

from assimilator.core.database.repository import Repository
from assimilator.core.patterns import ErrorWrapper


class UnitOfWork(ABC):
    error_wrapper: ErrorWrapper = ErrorWrapper()

    def __init__(self, repository: Repository, error_wrapper: Optional[ErrorWrapper] = None):
        self.repository = repository
        if error_wrapper is not None:
            self.error_wrapper = error_wrapper

        self.begin = self.error_wrapper.decorate(self.begin)
        self.rollback = self.error_wrapper.decorate(self.rollback)
        self.commit = self.error_wrapper.decorate(self.commit)
        self.close = self.error_wrapper.decorate(self.close)

    @abstractmethod
    def begin(self):
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError()

    @abstractmethod
    def commit(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
            self.close()
            raise exc_val
        else:
            self.close()

    def __str__(self):
        return f"{self.__class__.__name__}({self.repository.model})"

    def __repr__(self):
        return str(self)


__all__ = [
    'UnitOfWork',
]
