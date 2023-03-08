from typing import Optional

from pymongo.client_session import ClientSession

from assimilator.core.database import UnitOfWork
from assimilator.core.patterns import ErrorWrapper
from assimilator.mongo.database.repository import MongoRepository
from assimilator.mongo.database.error_wrapper import MongoErrorWrapper


class MongoUnitOfWork(UnitOfWork):
    repository: MongoRepository
    transaction: ClientSession

    def __init__(
        self,
        repository: MongoRepository,
        error_wrapper: Optional[ErrorWrapper] = None,
        autocommit: bool = False,
    ):
        super(MongoUnitOfWork, self).__init__(
            repository=repository,
            error_wrapper=error_wrapper or MongoErrorWrapper(),
            autocommit=autocommit,
        )

    def begin(self):
        self.transaction = self.repository.session.start_session()
        self.transaction.start_transaction()

    def rollback(self):
        self.transaction.abort_transaction()

    def commit(self):
        self.transaction.commit_transaction()

    def close(self):
        pass


__all__ = [
    'MongoUnitOfWork',
]
