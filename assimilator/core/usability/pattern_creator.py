from typing import TypeVar, Any, Callable

from assimilator.core.usability.registry import create_pattern
from assimilator.core.database import Repository, UnitOfWork
from assimilator.core.services import CRUDService

ModelT = TypeVar("ModelT")


def create_repository(
    provider: str,
    model: ModelT,
    session: Any,
    **kwargs,
) -> Repository:
    return create_pattern(
        provider=provider,
        pattern_name='repository',
        model=model,
        session=session,
        **kwargs,
    )


def create_uow(
    provider: str,
    model: ModelT,
    session: Any,
    repository_creator: Callable = create_repository,   # TODO: fix annotation
    **kwargs,
) -> UnitOfWork:
    repository = repository_creator(provider=provider, model=model, session=session)
    return create_pattern(
        provider=provider,
        pattern_name='uow',
        repository=repository,
        **kwargs,
    )


def create_crud_service(
    provider: str,
    model: ModelT,
    session: Any,
    **kwargs,
) -> CRUDService:
    uow = create_uow(provider=provider, model=model, session=session)
    return create_pattern(
        provider=provider,
        pattern_name='crud',
        uow=uow,
        **kwargs,
    )
