import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from assimilator.core.database import UnitOfWork
from assimilator.core.services import CRUDService
from assimilator.core.usability.registry import find_provider
from assimilator.core.usability.pattern_creator import create_uow, create_event_bus

from .crud import OrdersCRUD
from .database import Order, Base, OrderStatus

find_provider('assimilator.alchemy')
find_provider('assimilator.redis_')

engine = create_engine(url="sqlite:///orders_service.db")
SessionCreator = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

session = SessionCreator()

try:
    session.add(OrderStatus(status='created'))
    session.add(OrderStatus(status='rejected'))
    session.add(OrderStatus(status='shipped'))
    session.commit()
except Exception:
    session.rollback()
finally:
    session.close()


def get_uow() -> UnitOfWork:
    return create_uow(
        provider='alchemy',
        model=Order,
        session=SessionCreator(),
    )


def get_orders_crud() -> CRUDService:
    return OrdersCRUD(uow=get_uow(), event_producer=event_bus.producer)


kwargs = {"session": redis.Redis(port=9000)}
event_bus = create_event_bus(
    provider='redis',
    kwargs_producer=kwargs,
    kwargs_consumer=kwargs,
)
