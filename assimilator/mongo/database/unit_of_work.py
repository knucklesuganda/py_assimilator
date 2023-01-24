from pymongo.client_session import ClientSession

from assimilator.core.database import UnitOfWork
from assimilator.mongo.database.repository import MongoRepository


class MongoUnitOfWork(UnitOfWork):
    repository: MongoRepository
    transaction: ClientSession

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
