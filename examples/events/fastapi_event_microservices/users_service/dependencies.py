import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from assimilator.core.database import UnitOfWork
from assimilator.core.services import CRUDService
from assimilator.core.usability.registry import find_provider
from assimilator.core.usability.pattern_creator import create_uow, create_event_bus
from core.events.events_bus import EventBus

from .crud import UsersCRUD
from .database import User, Base

find_provider('assimilator.alchemy')
find_provider('assimilator.redis_')

engine = create_engine(url="sqlite:///users_service.db")
Base.metadata.create_all(engine)
SessionCreator = sessionmaker(bind=engine)
redis_client = redis.Redis(port=9000)


def get_uow() -> UnitOfWork:
    return create_uow(
        provider='alchemy',
        model=User,
        session=SessionCreator(),
    )


def get_users_crud() -> CRUDService:
    event_bus = get_event_bus()
    return UsersCRUD(uow=get_uow(), event_producer=event_bus.producer)


def get_event_bus() -> EventBus:
    kwargs = {'session': redis_client}
    return create_event_bus(provider='redis', kwargs_consumer=kwargs, kwargs_producer=kwargs)
