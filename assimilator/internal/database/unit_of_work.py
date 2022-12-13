from abc import ABC, abstractmethod

from assimilator.core.database.repository import BaseRepository


class DictUnitOfWork(ABC):
    def __init__(self, repository: BaseRepository):
        self.repository = repository
        self._saved_data = None

    @abstractmethod
    def begin(self):
        self._saved_data = self.repository.session
        self.repository.session = dict(self._saved_data)

    @abstractmethod
    def rollback(self):
        self.repository.session = self._saved_data

    @abstractmethod
    def commit(self):
        self._saved_data = self.repository.session

    @abstractmethod
    def close(self):
        pass
