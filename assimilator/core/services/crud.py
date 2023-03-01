from typing import TypeVar, Iterable, Union

from assimilator.core.database import UnitOfWork
from assimilator.core.services.base import Service
from assimilator.core.patterns import LazyCommand

ModelT = TypeVar("ModelT")


class CRUDService(Service):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self._specs = self.uow.repository.specs

    def create(self, obj_data: dict) -> ModelT:
        with self.uow:
            obj = self.uow.repository.save(**obj_data)
            self.uow.commit()

        self.uow.repository.refresh(obj)
        return obj

    def update(self, update_data: dict, *filters, **kwargs_filters) -> ModelT:
        with self.uow:
            obj = self.get(*filters, **kwargs_filters)

            for key, value in update_data.items():
                setattr(obj, key, value)

            self.uow.repository.update(obj)
            self.uow.commit()

        self.uow.repository.refresh(obj)
        return obj

    def list(
        self, *filters, lazy: bool = False, **kwargs_filters,
    ) -> Union[Iterable[ModelT], LazyCommand[Iterable[ModelT]]]:
        return self.uow.repository.filter(
            self._specs.filter(*filters, **kwargs_filters),
            lazy=lazy,
        )

    def get(self, *filters, lazy: bool = False, **kwargs_filters):
        return self.uow.repository.get(
            self._specs.filter(*filters, **kwargs_filters),
            lazy=lazy,
        )

    def delete(self, *filters, **kwargs_filters):
        with self.uow:
            obj = self.get(*filters, **kwargs_filters)
            self.uow.repository.delete(obj)
            self.uow.commit()

    def __str__(self):
        return f"CRUD({self.uow.repository.model})"


__all__ = [
    'CRUDService',
]
