import sys

import redis
import pymongo
from sqlalchemy.orm import sessionmaker

from core.usability.pattern_creator import create_uow
from examples.simple_database.models import engine, AlchemyUser, InternalUser, RedisUser, MongoUser


alchemy_session_creator = sessionmaker(bind=engine)
internal_session = {}


database_registry = {   # That is just one way of doing it, you can try whatever!
    'alchemy': {
        'model': AlchemyUser,
        'session_creator': lambda: alchemy_session_creator(),
        'init_kwargs': {},
    },
    'internal': {
        'model': InternalUser,
        'session_creator': lambda: internal_session,
        'init_kwargs': {},
    },
    'redis': {
        'model': RedisUser,
        'session_creator': lambda: redis.Redis(),
        'init_kwargs': {},
    },
    'mongo': {
        'model': MongoUser,
        'session_creator': lambda: pymongo.MongoClient(),
        'init_kwargs': {
            'database': 'assimilator_users',
        },
    }
}

database_provider = sys.argv[1] if len(sys.argv) > 1 else "alchemy"
User = database_registry[database_provider]['model']


def get_uow():
    dependencies = database_registry[database_provider]
    return create_uow(
        provider=database_provider,
        model=dependencies['model'],
        session=dependencies['session_creator'](),
        **dependencies['init_kwargs'],
    )
