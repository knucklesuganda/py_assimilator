from abc import ABC, abstractmethod
from typing import Union, Any, Optional, Callable, Iterable, Type

from assimilator.core.database.specifications import Specification, SpecificationList


class LazyCommand:
    def __init__(self, command: Callable, *args, **kwargs):
        self.command = command
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.command(*self.args, **self.kwargs)


class BaseRepository(ABC):
    def __init__(self, session: Any, specifications: Type[SpecificationList], initial_query: Optional[Any] = None):
        self.session = session
        self.initial_query = initial_query
        self.specifications = specifications

    def _get_initial_query(self):
        if self.initial_query is not None:
            return self.initial_query
        else:
            raise NotImplementedError("You must either pass the initial query or define get_initial_query()")

    def _apply_specifications(self, specifications: Iterable[Specification]) -> Any:
        query = self._get_initial_query()

        for specification in specifications:
            query = specification(query)

        return query

    @abstractmethod
    def get(self, *specifications: Specification, lazy: bool = False) -> Union[LazyCommand, Any]:
        raise NotImplementedError("get() is not implemented()")

    @abstractmethod
    def filter(self, *specifications: Specification, lazy: bool = False) -> Union[LazyCommand, Iterable]:
        raise NotImplementedError("filter() is not implemented()")

    @abstractmethod
    def save(self, obj) -> None:
        raise NotImplementedError("save() is not implemented in the repository")

    @abstractmethod
    def delete(self, obj) -> None:
        raise NotImplementedError("delete() is not implemented in the repository")

    @abstractmethod
    def update(self, obj) -> None:
        raise NotImplementedError("update() is not implemented in the repository")

    @abstractmethod
    def is_modified(self, obj) -> bool:
        raise NotImplementedError("is_modified() is not implemented in the repository")

    @abstractmethod
    def refresh(self, obj) -> None:
        raise NotImplementedError("refresh() is not implemented in the repository")


__all__ = [
    'LazyCommand',
    'BaseRepository',
]
