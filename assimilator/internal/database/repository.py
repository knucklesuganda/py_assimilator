import re

from assimilator.core.database import BaseRepository
from assimilator.core.database.exceptions import NotFoundError
from assimilator.internal.database.specifications import InternalSpecification, key_specification


class InternalRepository(BaseRepository):
    def __init__(self, session: dict):
        super(InternalRepository, self).__init__(session=session, initial_query='')

    def get(self, *specifications: InternalSpecification, lazy: bool = False):
        try:
            return self.session[self._apply_specifications(specifications)]
        except (KeyError, TypeError) as exc:
            raise NotFoundError(exc)

    def filter(self, *specifications: InternalSpecification, lazy: bool = False):
        key_mask = self._apply_specifications(specifications)

        if lazy:
            return key_mask

        models = []
        for key, value in self.session.items():
            if re.match(key, key_mask):
                models.append(value)

        return models

    def save(self, obj):
        obj_copy = obj.copy()
        self.session[str(obj_copy.id)] = obj_copy

    def delete(self, obj):
        del self.session[str(obj.id)]

    def update(self, obj):
        obj_copy = obj.copy()
        self.session[str(obj_copy.id)] = obj_copy

    def is_modified(self, obj):
        return self.get(key_specification(obj.id)) == obj

    def refresh(self, obj):
        obj.value = self.get(key_specification(obj.id))
