from redis.client import Redis

from assimilator.redis_ import RedisRepository, RedisUnitOfWork
from examples.redis.database.models import RedisUser

session = Redis()


def create_repository():    # factory for RedisRepository
    return RedisRepository(session=session, model=RedisUser)


def create_unit_of_work():  # factory for RedisUnitOfWork
    return RedisUnitOfWork(repository=create_repository())


__all__ = ['create_repository', 'create_unit_of_work']
