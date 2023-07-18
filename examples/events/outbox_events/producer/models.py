import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from assimilator.alchemy.events.models import create_event_model
from assimilator.alchemy.events.transactional_outbox import AlchemyTransactionalOutbox
from assimilator.core.usability.pattern_creator import create_event_producer, create_uow
from core.usability.registry import find_provider

find_provider('assimilator.redis_')

engine = create_engine(url="sqlite:///outbox_events.db")
Base = declarative_base()

event_model = create_event_model(base_cls=Base)
session_creator = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

events_uow = create_uow(provider='alchemy', model=event_model, session=session_creator())
producer = create_event_producer(provider='redis', kwargs_producer={"session": redis.Redis(port=9000)})
outbox = AlchemyTransactionalOutbox(
    event_model=event_model,
    producer=producer,
    events_uow=events_uow,
)

__all__ = [
    'events_uow',
    'producer',
    'outbox',
]
