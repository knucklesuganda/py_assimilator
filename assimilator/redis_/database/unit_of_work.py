from redis.client import Pipeline

from assimilator.core.database.unit_of_work import UnitOfWork
from redis_.database.repository import RedisRepository


class RedisUnitOfWork(UnitOfWork):
    repository: RedisRepository

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
