import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from assimilator.core.database import UnitOfWork
from assimilator.core.services import CRUDService
from assimilator.core.usability.pattern_creator import create_uow, create_event_producer
from assimilator.core.usability.registry import find_provider

from .crud import UsersCRUD
from .database import User, Base

find_provider('assimilator.alchemy')
find_provider('assimilator.redis_')

engine = create_engine(url="sqlite:///abcde.db")
Base.metadata.create_all(engine)
SessionCreator = sessionmaker(bind=engine)


def get_session():
    return SessionCreator()


def get_redis_session():
    return redis.Redis()


def get_uow() -> UnitOfWork:
    return create_uow(
        provider='alchemy',
        model=User,
        session=get_session(),
    )


def get_crud() -> CRUDService:
    return UsersCRUD(
        uow=get_uow(),
        event_producer=create_event_producer(
            provider='redis',
            kwargs_producer={
                'session': get_redis_session(),
            },
        )
    )
