from typing import Protocol, TypeVar, Type, Union, Collection, Optional

from assimilator.core.database import SpecificationType, SpecificationList
from assimilator.core.patterns import LazyCommand

QueryT = TypeVar("QueryT")
ModelT = TypeVar("ModelT")
SessionT = TypeVar("SessionT")
SpecsT = TypeVar("SpecsT", bound=Type[SpecificationList])


class RepositoryGetProtocol(Protocol):
    def __call__(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: QueryT = None,
    ) -> Union[ModelT, LazyCommand[ModelT]]:
        ...


class RepositoryFilterProtocol(Protocol):
    def __call__(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: QueryT = None,
    ) -> Union[Collection[ModelT], LazyCommand[Collection[ModelT]]]:
        ...


class RepositorySaveProtocol(Protocol):
    def __call__(
        self,
        obj: Optional[ModelT] = None,
        **obj_data: dict,
    ) -> ModelT:
        ...


class RepositoryDeleteProtocol(Protocol):
    def __call__(
        self,
        obj: Optional[ModelT] = None,
        *specifications: SpecificationType,
    ) -> None:
        ...


class RepositoryUpdateProtocol(Protocol):
    def __call__(
        self,
        obj: Optional[ModelT] = None,
        *specifications: SpecificationType,
        **update_values,
    ) -> None:
        ...


class RepositoryIsModifiedProtocol(Protocol):
    def __call__(self, obj: ModelT) -> bool:
        ...



class RepositoryRefreshProtocol(Protocol):
    def __call__(self, obj: ModelT) -> None:
        ...


class RepositoryCountProtocol(Protocol):
    def __call__(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: QueryT = None,
    ) -> Union[LazyCommand[int], int]:
        ...
