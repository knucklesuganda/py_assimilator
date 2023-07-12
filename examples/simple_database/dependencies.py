import sys

import redis
import pymongo
from sqlalchemy.orm import sessionmaker
from assimilator.core.usability.pattern_creator import create_uow

from examples.simple_database.models import engine, AlchemyUser, InternalUser, RedisUser, MongoUser


alchemy_session_creator = sessionmaker(bind=engine)
internal_session = {}


# Database registry contains all the possible patterns and their settings.
# We do that just as an example, you can try or do whatever you want!
database_registry = {
    'alchemy': {
        'model': AlchemyUser,   # Model to be used
        'session_creator': lambda: alchemy_session_creator(),   # function that can create sessions
        'kwargs_repository': {},    # Additional settings for the repository
    },
    'internal': {
        'model': InternalUser,
        'session_creator': lambda: internal_session,
        'kwargs_repository': {},
    },
    'redis': {
        'model': RedisUser,
        'session_creator': lambda: redis.Redis(),
        'kwargs_repository': {},
    },
    'mongo': {
        'model': MongoUser,
        'session_creator': lambda: pymongo.MongoClient(),
        'kwargs_repository': {
            'database': 'assimilator_users',
        },
    }
}

database_provider = sys.argv[1] if len(sys.argv) > 1 else "alchemy"     # get the provider from args
User = database_registry[database_provider]['model']    # get the model


def get_uow():
    dependencies = database_registry[database_provider]
    model = dependencies['model']
    session = dependencies['session_creator']()     # create a new connection to the database
    kwargs_repository = dependencies['kwargs_repository']

    return create_uow(
        provider=database_provider,
        model=model,
        session=session,
        kwargs_repository=kwargs_repository,
    )
