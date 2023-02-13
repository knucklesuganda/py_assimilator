from typing import Protocol, TypeVar, Optional, Iterable, Union, Any

QueryT = TypeVar("QueryT")


class OrderSpecificationProtocol(Protocol):
    def __call__(self, *clauses) -> QueryT:
        ...


class PaginateSpecificationProtocol(Protocol):
    def __call__(self, *, limit: Optional[int] = None, offset: Optional[int] = None):
        ...


class JoinSpecificationProtocol(Protocol):
    def __call__(self, *targets: Any, join_from: Optional[Any] = None, **join_args: dict):
        ...


class OnlySpecificationProtocol(Protocol):
    def __call__(self, *only_fields: Iterable[str]):
        ...


__all__ = [
    'OrderSpecificationProtocol',
    'PaginateSpecificationProtocol',
    'JoinSpecificationProtocol',
    'OnlySpecificationProtocol',
]
