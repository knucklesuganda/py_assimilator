from redis.client import Redis

from assimilator.redis_ import RedisRepository, RedisUnitOfWork
from examples.redis.database.models import RedisUser
from internal import InternalRepository, InternalUnitOfWork

# from examples.alchemy.database.dependencies import create_uow, create_repository

session = Redis()
# session = {}


def create_repository():    # factory for RedisRepository
    # return InternalRepository(session, model=RedisUser)
    return RedisRepository(session=session, model=RedisUser)


def create_uow():  # factory for RedisUnitOfWork
    # return InternalUnitOfWork(repository=create_repository())
    return RedisUnitOfWork(repository=create_repository())


__all__ = ['create_repository', 'create_uow']
