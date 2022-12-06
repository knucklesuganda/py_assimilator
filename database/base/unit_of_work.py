from abc import ABC, abstractmethod

from database.base.repository import BaseRepository


class UnitOfWork(ABC):
    def __init__(self, repository: BaseRepository):
        self.repository = repository

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
