from typing import Type

from assimilator.core.database import UnitOfWork
from assimilator.core.services.base import Service


class CRUDService(Service):
    def __init__(self, uow: UnitOfWork, model: Type):
        self.uow = uow
        self.specifications = self.uow.repository.specifications
        self.model = model

    def create(self, obj_data: dict):
        with self.uow:
            obj = self.model(**obj_data)
            self.uow.repository.save(obj)
            self.uow.commit()

        self.uow.repository.refresh(obj)
        return obj

    def update(self, update_data: dict, *filters, **kwargs_filters):
        with self.uow:
            obj = self.get(*filters, **kwargs_filters)

            for key, value in update_data.items():
                setattr(obj, key, value)

            self.uow.repository.update(obj)
            self.uow.commit()

        self.uow.repository.refresh(obj)
        return obj

    def list(self, *filters, lazy: bool = False, **kwargs_filters):
        return self.uow.repository.get(self.specifications.filter(*filters, **kwargs_filters), lazy=lazy)

    def get(self, *filters, lazy: bool = False, **kwargs_filters):
        return self.uow.repository.filter(self.specifications.filter(*filters, **kwargs_filters), lazy=lazy)

    def delete(self, *filters, **kwargs_filters):
        with self.uow:
            obj = self.get(*filters, **kwargs_filters)
            self.uow.repository.delete(obj)
            self.uow.commit()


__all__ = [
    'CRUDService',
]
