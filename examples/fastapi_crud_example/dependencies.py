import os

import pymongo
from redis.client import Redis
from sqlalchemy.orm import sessionmaker

from assimilator.alchemy.database import AlchemyRepository, AlchemyUnitOfWork
from assimilator.core.services import CRUDService
from assimilator.internal.database import InternalRepository, InternalUnitOfWork
from assimilator.mongo.database import MongoRepository, MongoUnitOfWork
from assimilator.redis_.database import RedisRepository, RedisUnitOfWork
from examples.fastapi_crud_example.models import (
    AlchemyBalance,
    AlchemyCurrency,
    AlchemyUser,
    InternalBalance,
    InternalCurrency,
    InternalUser,
    MongoBalance,
    MongoCurrency,
    MongoUser,
    RedisBalance,
    RedisCurrency,
    RedisUser,
    engine,
)

storage = os.environ.get("storage", "internal")


if storage == "alchemy":
    User = AlchemyUser
    Balance = AlchemyBalance
    Currency = AlchemyCurrency

    def get_uow():
        DatabaseSession = sessionmaker(bind=engine)
        repository = AlchemyRepository(
            session=DatabaseSession(),
            model=User,
        )
        return AlchemyUnitOfWork(repository)

elif storage == "internal":
    User = InternalUser
    Balance = InternalBalance
    Currency = InternalCurrency
    internal_session = {}

    def get_uow():
        repository = InternalRepository(internal_session, model=InternalUser)
        return InternalUnitOfWork(repository)

elif storage == "redis":
    redis_session = Redis()
    User = RedisUser
    Balance = RedisBalance
    Currency = RedisCurrency

    def get_uow():
        repository = RedisRepository(redis_session, model=User)
        return RedisUnitOfWork(repository)

elif storage == "mongo":
    User = MongoUser
    Balance = MongoBalance
    Currency = MongoCurrency
    mongo_client = pymongo.MongoClient()

    def get_uow():
        repository = MongoRepository(
            session=mongo_client, model=User, database="assimilator_fastapi"
        )
        return MongoUnitOfWork(repository)


def get_service():
    return CRUDService(uow=get_uow())
