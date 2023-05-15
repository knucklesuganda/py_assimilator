from typing import TypeVar, Iterable, Union

from assimilator.core.database import UnitOfWork, SpecificationList
from assimilator.core.services.base import Service
from assimilator.core.patterns import LazyCommand


ModelT = TypeVar("ModelT")


class CRUDService(Service):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self._specs: SpecificationList = self.uow.repository.specs

    def create(self, obj_data: Union[dict, ModelT]) -> ModelT:
        with self.uow:
            if isinstance(obj_data, dict):
                obj = self.uow.repository.save(**obj_data)
            else:
                obj = self.uow.repository.save(obj_data)

            self.uow.commit()

        self.uow.repository.refresh(obj)
        return obj

    def update(self, update_obj: Union[dict, ModelT], *filters, **kwargs_filters) -> ModelT:
        with self.uow:
            if isinstance(update_obj, dict):
                obj = self.get(*filters, **kwargs_filters)
                obj.__dict__.update(update_obj.__dict__)
                update_obj = obj

            self.uow.repository.update(update_obj)
            self.uow.commit()

        self.uow.repository.refresh(update_obj)
        return update_obj

    def list(
        self, *filters, lazy: bool = False, **kwargs_filters,
    ) -> Union[Iterable[ModelT], LazyCommand[Iterable[ModelT]]]:
        return self.uow.repository.filter(self._specs.filter(*filters, **kwargs_filters), lazy=lazy)

    def get(self, *filters, lazy: bool = False, **kwargs_filters) -> Union[ModelT, LazyCommand[ModelT]]:
        return self.uow.repository.get(self._specs.filter(*filters, **kwargs_filters), lazy=lazy)

    def delete(self, *filters, **kwargs_filters) -> None:
        with self.uow:
            obj = self.get(*filters, **kwargs_filters)
            self.uow.repository.delete(obj)
            self.uow.commit()

    def __str__(self):
        return f"CRUD({self.uow.repository.model})"


__all__ = [
    'CRUDService',
]
