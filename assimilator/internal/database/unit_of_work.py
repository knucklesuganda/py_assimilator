from copy import deepcopy
from typing import Optional

from assimilator.core.database import UnitOfWork, NotFoundError, DataLayerError, Repository
from assimilator.internal.database.error_wrapper import InternalErrorWrapper
from assimilator.core.patterns import ErrorWrapper


class InternalUnitOfWork(UnitOfWork):
    def __init__(
        self,
        repository: Repository,
        error_wrapper: Optional[ErrorWrapper] = None,
        autocommit: bool = False,
    ):
        super(InternalUnitOfWork, self).__init__(
            repository=repository,
            error_wrapper=error_wrapper or InternalErrorWrapper(),
            autocommit=autocommit,
        )
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
