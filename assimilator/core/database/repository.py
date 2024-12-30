from abc import ABC, abstractmethod
from functools import wraps
from typing import (
    Any,
    Callable,
    Collection,
    Dict,
    Generic,
    Iterable,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    final, Literal,
)

from assimilator.core.database.specifications.specifications import SpecificationType
from assimilator.core.database.typings import (
    ModelT,
    QueryT,
    RepositoryCountProtocol,
    RepositoryDeleteProtocol,
    RepositoryFilterProtocol,
    RepositoryGetProtocol,
    RepositoryIsModifiedProtocol,
    RepositoryRefreshProtocol,
    RepositorySaveProtocol,
    RepositoryUpdateProtocol,
    SessionT,
    SpecsT, RepositoryAggregateProtocol,
)
from assimilator.core.patterns.error_wrapper import ErrorWrapper
from assimilator.core.patterns.lazy_command import LazyCommand

T = TypeVar("T")


def make_lazy(func: Callable) -> Callable[..., Union["LazyCommand[T]", T]]:
    @wraps(func)
    def make_lazy_wrapper(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: QueryT | None = None,
    ) -> Union["LazyCommand[T]", T]:
        if lazy:
            return LazyCommand(
                func, self, *specifications, lazy=False, initial_query=initial_query
            )
        return func(self, *specifications, lazy=lazy, initial_query=initial_query)

    return make_lazy_wrapper


class Repository(Generic[SessionT, ModelT, QueryT, SpecsT], ABC):
    def __init__(
        self,
        session: SessionT,
        model: Type[ModelT],
        specifications: SpecsT,
        initial_query: Optional[QueryT] = None,
        error_wrapper: Optional[ErrorWrapper] = None,
    ):
        self.session = session
        self.model = model
        self.__initial_query: QueryT | None = initial_query
        self.specifications: SpecsT = specifications

        self.error_wrapper = error_wrapper or ErrorWrapper()
        self.get: RepositoryGetProtocol = LazyCommand.decorate(self.error_wrapper.decorate(self.get))
        self.filter: RepositoryFilterProtocol = LazyCommand.decorate(self.error_wrapper.decorate(self.filter))
        self.save: RepositorySaveProtocol = self.error_wrapper.decorate(self.save)
        self.delete: RepositoryDeleteProtocol = self.error_wrapper.decorate(self.delete)
        self.update: RepositoryUpdateProtocol = self.error_wrapper.decorate(self.update)
        self.is_modified: RepositoryIsModifiedProtocol = self.error_wrapper.decorate(self.is_modified)
        self.refresh: RepositoryRefreshProtocol = self.error_wrapper.decorate(self.refresh)
        self.count: RepositoryCountProtocol = LazyCommand.decorate(self.error_wrapper.decorate(self.count))
        self.aggregate: RepositoryAggregateProtocol = LazyCommand.decorate(self.error_wrapper.decorate(self.aggregate))

    @final
    def _check_obj_is_specification(
        self, obj: Optional[ModelT], specifications: Iterable[SpecificationType]
    ) -> Tuple[Optional[ModelT], Iterable[SpecificationType]]:
        """
        This function is called for parts of the
        code that use both obj and *specifications.
        We check that if the obj is a model
        """

        if not isinstance(obj, self.model) and (obj is not None):
            return None, (
                cast(SpecificationType, obj),
                *specifications,
            )  # obj is specification

        return obj, specifications

    @property
    def specs(self) -> SpecsT:
        """That property is used to shorten the full name of the self.specifications."""
        return self.specifications

    def get_initial_query(self, override_query: Optional[QueryT] = None) -> QueryT:
        if override_query is not None:
            return override_query
        elif self.__initial_query is not None:
            return self.__initial_query
        else:
            raise NotImplementedError(
                "You must either pass the initial query or define get_initial_query()"
            )

    def _get_specifications_context(self) -> Dict[str, Any]:
        return {"model": self.model, "repository": self}

    @abstractmethod
    def dict_to_models(self, data: dict) -> ModelT:
        """
        Converts data from Python dictionaries to models that Repository uses.
        You don't need to use that function directly 99% of the times.
        """
        raise NotImplementedError()

    @final
    def _apply_specifications(
        self,
        query: Union[QueryT, None],
        specifications: Iterable[SpecificationType],
    ) -> QueryT:
        query = self.get_initial_query(query)

        for specification in specifications:
            query = specification(query=query, **self._get_specifications_context())

        return query

    @abstractmethod
    def get(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: QueryT = None,
    ) -> Union[ModelT, LazyCommand[ModelT]]:
        raise NotImplementedError("get() is not implemented")

    @abstractmethod
    def aggregate(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: QueryT = None,
        result_type: Literal['single', 'all'] = 'single',
    ) -> Any:
        raise NotImplementedError("aggregate() is not implemented")

    @abstractmethod
    def filter(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: QueryT = None,
    ) -> Union[Collection[ModelT], LazyCommand[Collection[ModelT]]]:
        raise NotImplementedError("filter() is not implemented")

    @abstractmethod
    def save(self, obj: Optional[ModelT] = None, **obj_data: dict) -> ModelT:
        raise NotImplementedError("save() is not implemented in the repository")

    @abstractmethod
    def delete(
        self, obj: Optional[ModelT] = None, *specifications: SpecificationType
    ) -> None:
        raise NotImplementedError("delete() is not implemented in the repository")

    @abstractmethod
    def update(
        self,
        obj: Optional[ModelT] = None,
        *specifications: SpecificationType,
        **update_values,
    ) -> None:
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
        initial_query: QueryT = None,
    ) -> Union[LazyCommand[int], int]:
        raise NotImplementedError("count() is not implemented in the repository")

    def __str__(self):
        return f"{self.__class__.__name__}({self.model})"

    def __repr__(self):
        return str(self)


__all__ = [
    "LazyCommand",
    "Repository",
    "make_lazy",
]
