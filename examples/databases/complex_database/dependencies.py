import sys

import pymongo
from redis.client import Redis
from sqlalchemy.orm import sessionmaker

from assimilator.alchemy.database import AlchemyUnitOfWork, AlchemyRepository
from assimilator.internal.database import InternalRepository, InternalUnitOfWork
from assimilator.redis_.database import RedisRepository, RedisUnitOfWork
from assimilator.mongo.database import MongoRepository, MongoUnitOfWork

from examples.databases.complex_database.models import (
    engine, AlchemyUser, AlchemyUserBalance, AlchemyBalanceCurrency,
    InternalUser, InternalBalance, InternalCurrency,
    RedisUser, RedisBalance, RedisCurrency,
    MongoUser, MongoCurrency, MongoBalance,
)

if len(sys.argv) == 1 or sys.argv[1] == "alchemy":
    User = AlchemyUser
    Balance = AlchemyUserBalance
    Currency = AlchemyBalanceCurrency


    def get_uow():
        DatabaseSession = sessionmaker(bind=engine)
        repository = AlchemyRepository(
            session=DatabaseSession(),
            model=User,
        )
        return AlchemyUnitOfWork(repository)

elif sys.argv[1] == "internal":
    User = InternalUser
    Balance = InternalBalance
    Currency = InternalCurrency
    internal_session = {}

    def get_uow():
        repository = InternalRepository(internal_session, model=InternalUser)
        return InternalUnitOfWork(repository)

elif sys.argv[1] == "redis":
    redis_session = Redis()
    User = RedisUser
    Balance = RedisBalance
    Currency = RedisCurrency


    def get_uow():
        repository = RedisRepository(redis_session, model=User)
        return RedisUnitOfWork(repository)


    redis_session.flushdb()

elif sys.argv[1] == "mongo":
    User = MongoUser
    Balance = MongoBalance
    Currency = MongoCurrency
    mongo_client = pymongo.MongoClient()

    mongo_client['assimilator_complex'].drop_collection(MongoUser.AssimilatorConfig.collection)


    def get_uow():
        repository = MongoRepository(session=mongo_client, model=User, database='assimilator_complex')
        return MongoUnitOfWork(repository)
