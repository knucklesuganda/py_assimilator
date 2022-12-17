from assimilator.core.database import UnitOfWork
from assimilator.core.database.repository import BaseRepository


class InternalUnitOfWork(UnitOfWork):
    def __init__(self, repository: BaseRepository):
        super(InternalUnitOfWork, self).__init__(repository)
        self._saved_data = None

    def begin(self):
        self._saved_data = self.repository.session
        self.repository.session = dict(self._saved_data)

    def rollback(self):
        self.repository.session = self._saved_data

    def commit(self):
        self._saved_data = dict(self.repository.session)
        self.repository.session = self._saved_data

    def close(self):
        self._saved_data = None


__all__ = [
    'InternalUnitOfWork',
]
