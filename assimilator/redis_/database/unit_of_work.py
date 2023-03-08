from typing import Optional

from assimilator.core.patterns import ErrorWrapper
from assimilator.core.database.unit_of_work import UnitOfWork
from assimilator.redis_.database.repository import RedisRepository
from assimilator.internal.database.error_wrapper import InternalErrorWrapper


class RedisUnitOfWork(UnitOfWork):
    repository: RedisRepository

    def __init__(
        self,
        repository: RedisRepository,
        error_wrapper: Optional[ErrorWrapper] = None,
        autocommit: bool = False,
    ):
        super(RedisUnitOfWork, self).__init__(
            repository=repository,
            error_wrapper=error_wrapper or InternalErrorWrapper(),
            autocommit=autocommit,
        )

    def begin(self):
        self.repository.transaction = self.repository.session.pipeline()

    def rollback(self):
        self.repository.transaction.discard()

    def commit(self):
        self.repository.transaction.execute()

    def close(self):
        self.repository.transaction.reset()
        self.repository.transaction = self.repository.session


__all__ = [
    'RedisUnitOfWork',
]
