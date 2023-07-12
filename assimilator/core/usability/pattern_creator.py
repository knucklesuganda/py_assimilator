from typing import TypeVar, Any, Type, Dict, Optional, Iterable

from assimilator.core.events.events import Event
from assimilator.core.services import CRUDService
from assimilator.core.usability.registry import get_pattern
from assimilator.core.database import Repository, UnitOfWork
from assimilator.core.events.types import EventCallbackContainer
from assimilator.core.events.events_bus import EventConsumer, EventProducer, EventBus

ModelT = TypeVar("ModelT")


def create_repository(
    provider: str,
    model: Type[ModelT],
    session: Any,
    kwargs_repository: Dict[str, Any] = None,
) -> Repository:
    repository_cls: Type[Repository] = get_pattern(provider=provider, pattern_name='repository')
    return repository_cls(model=model, session=session, **(kwargs_repository or {}))


def create_uow(
    provider: str,
    model: Type[ModelT],
    session: Any,
    kwargs_repository: Dict[str, Any] = None,
    kwargs_uow: Dict[str, Any] = None,
) -> UnitOfWork:
    """

    :rtype: object
    """
    repository = create_repository(
        provider=provider,
        model=model,
        session=session,
        kwargs_repository=kwargs_repository,
    )
    uow_cls: Type[UnitOfWork] = get_pattern(provider=provider, pattern_name='uow')
    return uow_cls(repository=repository, **(kwargs_uow or {}))


def create_crud(
    provider: str,
    model: Type[ModelT],
    session: Any,
    kwargs_repository: Dict[str, Any] = None,
    kwargs_uow: Dict[str, Any] = None,
) -> CRUDService:
    uow = create_uow(
        provider=provider,
        model=model,
        session=session,
        kwargs_repository=kwargs_repository,
        kwargs_uow=kwargs_uow,
    )
    crud_cls: Type[CRUDService] = get_pattern(provider=provider, pattern_name='crud')
    return crud_cls(uow=uow)


def create_event_consumer(
    provider: str,
    callbacks: Optional[EventCallbackContainer] = None,
    events: Optional[Iterable[Type[Event]]] = None,
    kwargs_consumer: Dict[str, Any] = None,
) -> EventConsumer:
    consumer_cls: Type[EventConsumer] = get_pattern(provider=provider, pattern_name='event_consumer')
    return consumer_cls(callbacks=callbacks, events=events, **(kwargs_consumer or {}))


def create_event_producer(provider: str, kwargs_producer: Dict[str, Any] = None) -> EventProducer:
    producer_cls: Type[EventProducer] = get_pattern(provider=provider, pattern_name='event_producer')
    return producer_cls(**(kwargs_producer or {}))


def create_event_bus(
    provider: str,
    callbacks: Optional[EventCallbackContainer] = None,
    events: Optional[Iterable[Type[Event]]] = None,
    kwargs_consumer: Dict[str, Any] = None,
    kwargs_producer: Dict[str, Any] = None,
):
    producer = create_event_producer(provider=provider, kwargs_producer=kwargs_producer)
    consumer = create_event_consumer(
        provider=provider,
        callbacks=callbacks,
        events=events,
        kwargs_consumer=kwargs_consumer,
    )

    event_bus_cls: Type[EventBus] = get_pattern(provider=provider, pattern_name='event_bus')
    return event_bus_cls(producer=producer, consumer=consumer)
