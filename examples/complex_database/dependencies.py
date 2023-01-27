import sys

from redis.client import Redis
from sqlalchemy.orm import sessionmaker

from assimilator.alchemy.database import AlchemyUnitOfWork, AlchemyRepository
from assimilator.internal.database import InternalRepository, InternalUnitOfWork
from assimilator.redis_.database import RedisRepository, RedisUnitOfWork
from examples.complex_database.models import engine, AlchemyUser, AlchemyUserBalance


def get_alchemy_uow():
    DatabaseSession = sessionmaker(bind=engine)
    repository = AlchemyRepository(
        session=DatabaseSession(),
        model=User,
    )
    return AlchemyUnitOfWork(repository)


internal_session = {}


def get_internal_uow():
    """repository = InternalRepository(internal_session, model=InternalUser)"""
    """return InternalUnitOfWork(repository)"""


redis_session = Redis()


def get_redis_uow():
    """repository = RedisRepository(redis_session, model=RedisUser)"""
    """return RedisUnitOfWork(repository)"""


if len(sys.argv) == 1 or sys.argv[1] == "alchemy":
    User = AlchemyUser
    Balance = AlchemyUserBalance
    get_uow = get_alchemy_uow
# elif sys.argv[1] == "internal":
#     User = InternalUser
#     get_uow = get_internal_uow
# elif sys.argv[1] == "redis":
#     User = RedisUser
#     get_uow = get_redis_uow
#     redis_session.flushdb()
