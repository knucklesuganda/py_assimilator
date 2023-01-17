from functools import wraps
from typing import TypeVar, Callable, Generic, final
from abc import ABC, abstractmethod
from typing import Union, Optional, Iterable, Type, Collection

from assimilator.core.patterns.lazy_command import LazyCommand
from assimilator.core.database.specifications import SpecificationList, SpecificationType


def make_lazy(func: Callable):

    @wraps(func)
    def make_lazy_wrapper(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: QueryT = None,
    ):
        if lazy:
            return LazyCommand(func, self, *specifications, lazy=False, initial_query=initial_query)
        return func(*specifications, lazy=False, initial_query=initial_query)

    return make_lazy_wrapper


QueryT = TypeVar("QueryT")
ModelT = TypeVar("ModelT")
SessionT = TypeVar("SessionT")


class BaseRepository(Generic[SessionT, ModelT, QueryT], ABC):
    def __init__(
        self,
        session: SessionT,
        model: Type[ModelT],
        specifications: Type[SpecificationList],
        initial_query: Optional[SessionT] = None,
    ):
        self.session = session
        self.model = model
        self.__initial_query: QueryT = initial_query
        self.specifications = specifications

    @property
    def specs(self) -> Type[SpecificationList]:
        """ That property is used to shorten the full name of the self.specifications. """
        return self.specifications

    def get_initial_query(self, override_query: Optional[QueryT] = None) -> QueryT:
        if override_query is not None:
            return override_query
        elif self.__initial_query is not None:
            return self.__initial_query
        else:
            raise NotImplementedError("You must either pass the initial query or define get_initial_query()")

    @final
    def _apply_specifications(self, query: QueryT, specifications: Iterable[SpecificationType]) -> QueryT:
        for specification in specifications:
            query = specification(query)

        return query

    @abstractmethod
    def get(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: QueryT = None,
    ) -> Union[ModelT, LazyCommand[ModelT]]:
        raise NotImplementedError("get() is not implemented()")

    @abstractmethod
    def filter(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: QueryT = None,
    ) -> Union[Collection[ModelT], LazyCommand[Collection[ModelT]]]:
        raise NotImplementedError("filter() is not implemented()")

    @abstractmethod
    def save(self, obj: ModelT) -> None:
        raise NotImplementedError("save() is not implemented in the repository")

    @abstractmethod
    def delete(self, obj: ModelT) -> None:
        raise NotImplementedError("delete() is not implemented in the repository")

    @abstractmethod
    def update(self, obj: ModelT) -> None:
        raise NotImplementedError("update() is not implemented in the repository")

    @abstractmethod
    def is_modified(self, obj: ModelT) -> bool:
        raise NotImplementedError("is_modified() is not implemented in the repository")

    @abstractmethod
    def refresh(self, obj: ModelT) -> None:
        raise NotImplementedError("refresh() is not implemented in the repository")

    @abstractmethod
    def count(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
    ) -> Union[LazyCommand[int], int]:
        raise NotImplementedError("count() is not implemented in the repository")


__all__ = [
    'LazyCommand',
    'BaseRepository',
    'make_lazy',
]
