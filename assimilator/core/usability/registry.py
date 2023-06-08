from typing import Dict, Any, Literal, Type

from pydantic import BaseModel

from assimilator.core.database import Repository, UnitOfWork
from assimilator.core.services.crud import CRUDService


class PatternList(BaseModel):
    class Config:
        frozen = True

    repository: Type[Repository]
    uow: Type[UnitOfWork]
    crud: Type[CRUDService]


registry: Dict[str, PatternList] = {}


def register_pattern(provider: str, pattern_list: PatternList):
    registry[provider] = pattern_list


def get_pattern_list(provider: str):
    return registry[provider]


def unregister_pattern(name: str):
    del registry[name]


def create_pattern(
    provider: str,
    pattern_name: Literal['uow', 'repository', 'crud'],
    *init_args,
    **init_kwargs,
) -> Any:
    return getattr(registry[provider], pattern_name)(*init_args, **init_kwargs)


__all__ = [
    'create_pattern',
    'register_pattern',
    'unregister_pattern',
    'PatternList',
    'get_pattern_list',
]
