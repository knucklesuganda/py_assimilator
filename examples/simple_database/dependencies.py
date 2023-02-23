import sys

import pymongo
from redis.client import Redis
from sqlalchemy.orm import sessionmaker

from assimilator.alchemy.database import AlchemyUnitOfWork, AlchemyRepository
from assimilator.internal.database import InternalRepository, InternalUnitOfWork
from assimilator.redis_.database import RedisRepository, RedisUnitOfWork
from examples.simple_database.models import engine, AlchemyUser, InternalUser, RedisUser, MongoUser
from assimilator.mongo.database import MongoRepository, MongoUnitOfWork

if len(sys.argv) == 1 or sys.argv[1] == "alchemy":
    User = AlchemyUser

    def get_uow():
        DatabaseSession = sessionmaker(bind=engine)
        repository = AlchemyRepository(
            session=DatabaseSession(),
            model=User,
        )
        return AlchemyUnitOfWork(repository)

elif sys.argv[1] == "internal":
    User = InternalUser
    internal_session = {}

    def get_uow():
        repository = InternalRepository(internal_session, model=InternalUser)
        return InternalUnitOfWork(repository)

elif sys.argv[1] == "redis":
    User = RedisUser
    redis_session = Redis()
    redis_session.flushdb()

    def get_uow():
        repository = RedisRepository(redis_session, model=RedisUser)
        return RedisUnitOfWork(repository)

elif sys.argv[1] == "mongo":
    User = MongoUser
    client = pymongo.MongoClient()

    client['test'].drop_collection(MongoUser.AssimilatorConfig.collection)

    def get_uow():
        repository = MongoRepository(session=client, model=MongoUser, database='test')
        return MongoUnitOfWork(repository)
