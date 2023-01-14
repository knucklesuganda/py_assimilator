from abc import ABC, abstractmethod
from typing import Union, Any, Optional, Callable, Iterable, Type, Container

from assimilator.core.database.specifications import SpecificationList, SpecificationType


class LazyCommand:
    def __init__(self, command: Callable, *args, **kwargs):
        self.command = command
        self.args = args
        self.kwargs = kwargs
        self._results = None

    def __call__(self) -> Union[Container, Any]:
        if self._results is not None:
            return self._results

        self._results = self.command(*self.args, **self.kwargs)
        return self._results

    def __iter__(self):
        results = self()

        if not isinstance(results, Iterable):  # get() command
            raise StopIteration("Results are not iterable")

        return iter(results)  # filter() command

    def __bool__(self):
        return bool(self())


class BaseRepository(ABC):
    def __init__(
        self,
        session: Any,
        model: Type,
        specifications: Type[SpecificationList],
        initial_query: Optional[Any] = None,
    ):
        self.session = session
        self.model = model
        self.__initial_query = initial_query
        self.specifications = specifications

    @property
    def specs(self):
        """ That property is used to shorten the full name of the self.specifications. You can use any of them """
        return self.specifications

    def _get_initial_query(self):
        if self.__initial_query is not None:
            return self.__initial_query
        else:
            raise NotImplementedError("You must either pass the initial query or define get_initial_query()")

    def _apply_specifications(self, specifications: Iterable[SpecificationType], initial_query=None) -> Any:
        query = self._get_initial_query() if initial_query is None else initial_query

        for specification in specifications:
            query = specification(query)

        return query

    @abstractmethod
    def get(self, *specifications: SpecificationType, lazy: bool = False, initial_query=None)\
            -> Union[LazyCommand, Any]:
        raise NotImplementedError("get() is not implemented()")

    @abstractmethod
    def filter(self, *specifications: SpecificationType, lazy: bool = False, initial_query=None)\
            -> Union[LazyCommand, Container]:
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

    @abstractmethod
    def count(self, *specifications: SpecificationType, lazy: bool = False) -> Union[LazyCommand, int]:
        raise NotImplementedError("count() is not implemented in the repository")


__all__ = [
    'LazyCommand',
    'BaseRepository',
]
