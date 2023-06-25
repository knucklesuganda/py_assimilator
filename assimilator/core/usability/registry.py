import importlib
from typing import Dict, Type, Union

from pydantic import BaseModel

from assimilator.core.services.crud import CRUDService
from assimilator.core.database import Repository, UnitOfWork
from assimilator.core.usability.exceptions import PatternNotFoundError, ProviderNotFoundError


class PatternList(BaseModel):
    class Config:
        frozen = True

    repository: Type[Repository]
    uow: Type[UnitOfWork]
    crud: Type[CRUDService]


registry: Dict[str, PatternList] = {}


def register_pattern(provider: str, pattern_list: PatternList):
    registry[provider] = pattern_list


def find_patterns(provider_path: str):
    """ Imports a module that has automatic pattern registration """
    importlib.import_module(provider_path)


def get_pattern_list(provider: str):
    return registry[provider]


def unregister_pattern(name: str):
    del registry[name]


def get_pattern(provider: str, pattern_name: str) -> Type[Union[Repository, UnitOfWork, CRUDService]]:
    try:
        pattern_cls = getattr(registry[provider], pattern_name, None)
    except KeyError:
        raise ProviderNotFoundError(f"Provider {pattern_name} was not found")

    if pattern_cls is None:
        raise PatternNotFoundError(f"Pattern '{pattern_name}' for {provider} provider was not found")

    return pattern_cls


__all__ = [
    'register_pattern',
    'unregister_pattern',
    'PatternList',
    'get_pattern_list',
    'get_pattern',
    'find_patterns',
]
