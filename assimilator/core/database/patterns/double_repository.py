from typing import Union, Optional, Collection, TypeVar

from assimilator.core.database.repository import Repository
from assimilator.core.database import SpecificationType, DataLayerError
from assimilator.core.patterns import LazyCommand


QueryT = TypeVar("QueryT")
ModelT = TypeVar("ModelT")


class DoubleRepository(Repository):
    def __init__(self, primary: Repository, secondary: Repository, favor_primary: bool = True):
        super(DoubleRepository, self).__init__(
            session=primary.session,
            model=primary.model,
            specifications=primary.specifications,
            initial_query=primary.get_initial_query(),
            error_wrapper=primary.error_wrapper,
        )
        self.primary = primary
        self.secondary = secondary
        self.favor_primary = favor_primary

    @property
    def favored_repository(self) -> Repository:
        return self.primary if self.favor_primary else self.secondary

    def get(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: QueryT = None,
    ) -> Union[ModelT, LazyCommand[ModelT]]:
        try:
            return self.secondary.get(*specifications, lazy=False, initial_query=initial_query)
        except DataLayerError:
            return self.primary.get(*specifications, lazy=False, initial_query=initial_query)

    def filter(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: QueryT = None
    ) -> Union[Collection[ModelT], LazyCommand[Collection[ModelT]]]:
        try:
            return self.secondary.filter(*specifications, lazy=False, initial_query=initial_query)
        except DataLayerError:
            return self.primary.filter(*specifications, lazy=False, initial_query=initial_query)

    def save(self, obj: Optional[ModelT] = None, **obj_data) -> ModelT:
        return_data = self.primary.save(obj=obj, **obj_data)
        self.secondary.save(obj=obj, **obj_data)
        return return_data

    def delete(self, obj: Optional[ModelT] = None, *specifications: SpecificationType) -> None:
        return_data = self.primary.delete(obj=obj, *specifications)
        self.secondary.delete(obj=obj, *specifications)
        return return_data

    def update(self, obj: Optional[ModelT] = None, *specifications: SpecificationType, **update_values) -> None:
        return_data = self.primary.update(obj=obj, *specifications)
        self.secondary.update(obj=obj, *specifications)
        return return_data

    def is_modified(self, obj: ModelT) -> bool:
        return self.favored_repository.is_modified(obj=obj)

    def refresh(self, obj: ModelT) -> None:
        return self.favored_repository.refresh(obj=obj)

    def count(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: QueryT = None,
    ) -> Union[LazyCommand[int], int]:
        return self.favored_repository.count(*specifications, lazy=False, initial_query=initial_query)


__all__ = ['DoubleRepository']
