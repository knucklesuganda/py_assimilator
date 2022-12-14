from copy import deepcopy
from typing import Optional

from assimilator.core.database import UnitOfWork
from assimilator.core.database.repository import BaseRepository


class InternalUnitOfWork(UnitOfWork):
    def __init__(self, repository: BaseRepository):
        super(InternalUnitOfWork, self).__init__(repository)
        self._saved_data: Optional[dict] = None

    def begin(self):
        self._saved_data = self.repository.session
        self.repository.session = deepcopy(self._saved_data)

    def rollback(self):
        self.repository.session = self._saved_data

    def commit(self):
        self._saved_data.update(self.repository.session)

        for deleted_key in set(self._saved_data.keys()) - set(self.repository.session.keys()):
            del self._saved_data[deleted_key]

        self.repository.session = self._saved_data

    def close(self):
        self._saved_data = None


__all__ = [
    'InternalUnitOfWork',
]
