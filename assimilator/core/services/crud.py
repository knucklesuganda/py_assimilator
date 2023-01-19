from typing import Type

from assimilator.core.database import UnitOfWork
from assimilator.core.services.base import Service


class CRUDService(Service):
    def __init__(self, model: Type):
        self.model = model

    def create(self, obj_data: dict, uow: UnitOfWork):
        with uow:
            obj = self.model(**obj_data)
            uow.repository.save(obj)
            uow.commit()

        uow.repository.refresh(obj)
        return obj

    def update(self, update_data: dict, uow: UnitOfWork, *filters, **kwargs_filters):
        with uow:
            obj = self.get(*filters, **kwargs_filters)

            for key, value in update_data.items():
                setattr(obj, key, value)

            uow.repository.update(obj)
            uow.commit()

        uow.repository.refresh(obj)
        return obj

    def list(self, *filters, uow: UnitOfWork, lazy: bool = False, **kwargs_filters):
        return uow.repository.get(uow.repository.specs.filter(*filters, **kwargs_filters), lazy=lazy)

    def get(self, *filters, uow: UnitOfWork, lazy: bool = False, **kwargs_filters):
        return uow.repository.filter(uow.repository.specs.filter(*filters, **kwargs_filters), lazy=lazy)

    def delete(self, uow: UnitOfWork, *filters, **kwargs_filters):
        with uow:
            obj = self.get(*filters, **kwargs_filters)
            uow.repository.delete(obj)
            uow.commit()


__all__ = [
    'CRUDService',
]
