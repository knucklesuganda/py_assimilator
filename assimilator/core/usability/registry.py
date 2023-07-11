import importlib
from typing import Dict, Type, Union

from pydantic import BaseModel, Extra

from assimilator.core.services.crud import CRUDService
from assimilator.core.database import Repository, UnitOfWork
from assimilator.core.events.events_bus import EventConsumer, EventProducer, EventBus
from assimilator.core.usability.exceptions import PatternNotFoundError, ProviderNotFoundError


class PatternList(BaseModel):
    class Config:
        frozen = True
        extra = Extra.allow

    repository: Type[Repository] = None
    uow: Type[UnitOfWork] = None
    crud: Type[CRUDService] = CRUDService
    event_consumer: Type[EventConsumer] = None
    event_producer: Type[EventProducer] = None
    event_bus: Type[EventBus] = EventBus


registry: Dict[str, PatternList] = {}


def register_provider(provider: str, pattern_list: PatternList):
    registry[provider] = pattern_list


def find_provider(provider_path: str):
    """ Imports a module that has automatic pattern registration """
    importlib.import_module(provider_path)


def get_pattern_list(provider: str):
    return registry[provider]


def unregister_provider(provider: str):
    try:
        del registry[provider]
    except KeyError:
        raise ProviderNotFoundError(f"Provider {provider} was not found")


def get_pattern(provider: str, pattern_name: str) -> Type[Union[
    Repository, UnitOfWork, CRUDService,
    EventConsumer, EventProducer, EventBus,
]]:
    try:
        pattern_cls = getattr(registry[provider], pattern_name, None)
    except KeyError:
        raise ProviderNotFoundError(f"Provider {provider} was not found")

    if pattern_cls is None:
        raise PatternNotFoundError(f"Pattern '{pattern_name}' for {provider} provider was not found")

    return pattern_cls


__all__ = [
    'register_provider',
    'unregister_provider',
    'PatternList',
    'get_pattern_list',
    'get_pattern',
    'find_provider',
]
