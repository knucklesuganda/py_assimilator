import os

import pymongo
from redis.client import Redis
from sqlalchemy.orm import sessionmaker

from assimilator.alchemy.database import AlchemyUnitOfWork, AlchemyRepository
from assimilator.internal.database import InternalRepository, InternalUnitOfWork
from assimilator.redis_.database import RedisRepository, RedisUnitOfWork
from assimilator.mongo.database import MongoRepository, MongoUnitOfWork
from assimilator.core.services import CRUDService

from examples.complex_database.models import (
    engine, AlchemyUser, AlchemyUserBalance, AlchemyBalanceCurrency,
    InternalUser, InternalBalance, InternalCurrency,
    RedisUser, RedisBalance, RedisCurrency,
    MongoUser, MongoCurrency, MongoBalance,
)
from examples.fastapi_crud_example.models import mapper_registry

storage = os.environ.get('storage', 'alchemy')


if storage == "alchemy":
    User = AlchemyUser
    Balance = AlchemyUserBalance
    Currency = AlchemyBalanceCurrency
    mapper_registry.metadata.create_all(engine)

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

    redis_session.flushdb()

elif storage == "mongo":
    User = MongoUser
    Balance = MongoBalance
    Currency = MongoCurrency
    mongo_client = pymongo.MongoClient()

    mongo_client['assimilator_complex'].drop_collection(MongoUser.AssimilatorConfig.collection)

    def get_uow():
        repository = MongoRepository(session=mongo_client, model=User, database='assimilator_complex')
        return MongoUnitOfWork(repository)


def get_service():
    return CRUDService(uow=get_uow())
