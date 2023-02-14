from typing import Protocol, TypeVar, Optional, Iterable, Any

QueryT = TypeVar("QueryT")


class OrderSpecificationProtocol(Protocol):
    def __call__(self, *clauses: str) -> QueryT:
        ...


class PaginateSpecificationProtocol(Protocol):
    def __call__(self, *, limit: Optional[int] = None, offset: Optional[int] = None):
        ...


class JoinSpecificationProtocol(Protocol):
    def __call__(self, *targets: Any, join_from: Optional[Any] = None, join_args: Iterable[dict]):
        ...


class OnlySpecificationProtocol(Protocol):
    def __call__(self, *only_fields: Iterable[str]) -> Iterable[QueryT]:
        ...


__all__ = [
    'OrderSpecificationProtocol',
    'PaginateSpecificationProtocol',
    'JoinSpecificationProtocol',
    'OnlySpecificationProtocol',
]
