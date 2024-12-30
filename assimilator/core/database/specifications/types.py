from typing import Any, Iterable, Optional, Protocol, TypeVar

QueryT = TypeVar("QueryT", covariant=True)


class OrderSpecificationProtocol(Protocol[QueryT]):
    def __call__(self, *clauses: str) -> QueryT: ...


class PaginateSpecificationProtocol(Protocol):
    def __call__(
        self, *, limit: Optional[int] = None, offset: Optional[int] = None
    ): ...


class JoinSpecificationProtocol(Protocol):
    def __call__(self, *targets: Any, join_args: Iterable[dict] | None = None): ...


class OnlySpecificationProtocol(Protocol):
    def __call__(self, *only_fields: Iterable[str]) -> Iterable[QueryT]: ...


__all__ = [
    "OrderSpecificationProtocol",
    "PaginateSpecificationProtocol",
    "JoinSpecificationProtocol",
    "OnlySpecificationProtocol",
]
