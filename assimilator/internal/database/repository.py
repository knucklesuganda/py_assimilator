import re
from typing import Type

from assimilator.core.database import BaseRepository, SpecificationList
from assimilator.core.database.exceptions import NotFoundError
from assimilator.internal.database.specifications import InternalSpecification, InternalSpecificationList


class InternalRepository(BaseRepository):
    def __init__(self, session: dict, specifications: Type[SpecificationList] = InternalSpecificationList):
        super(InternalRepository, self).__init__(session=session, initial_query='', specifications=specifications)

    def get(self, *specifications: InternalSpecification, lazy: bool = False):
        try:
            return self.session[self._apply_specifications(specifications)]
        except (KeyError, TypeError) as exc:
            raise NotFoundError(exc)

    def filter(self, *specifications: InternalSpecification, lazy: bool = False):
        if not specifications:
            return list(self.session.values())

        key_mask = self._apply_specifications(specifications)
        if lazy:
            return key_mask

        models = []
        for key, value in self.session.items():
            if not re.match(key, key_mask):
                pass

            models.append(value)

        return models

    def save(self, obj):
        self.session[str(obj.id)] = obj

    def delete(self, obj):
        del self.session[str(obj.id)]

    def update(self, obj):
        self.session[str(obj.id)] = obj

    def is_modified(self, obj):
        return self.get(self.specifications.filter(obj.id)) == obj

    def refresh(self, obj):
        obj.value = self.get(self.specifications.filter(obj.id))


__all__ = [
    'InternalRepository',
]
