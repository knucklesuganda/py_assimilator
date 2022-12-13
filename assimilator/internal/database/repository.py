import re
from typing import Iterable, Any, Type, Union

from pydantic import BaseModel

from assimilator.core.database import BaseRepository, Specification
from assimilator.core.database.exceptions import NotFoundError
from assimilator.internal.database.specifications import DictSpecification, DictKeySpecification


class DictModel(BaseModel):
    id: str
    value: Any


class InternalRepository(BaseRepository):
    def __init__(self, session: dict, model: Type[DictModel] = DictModel):
        super(InternalRepository, self).__init__(session)
        self.model = model

    def get_initial_query(self):
        return ''

    def get(self, *specifications: DictSpecification, lazy: bool = False):
        try:
            return self.session[self.apply_specifications(specifications)]
        except (KeyError, TypeError) as exc:
            raise NotFoundError(exc)

    def filter(self, *specifications: DictSpecification, lazy: bool = False):
        models = []
        key_mask = self.apply_specifications(specifications)

        for key, value in self.session.items():
            if re.match(key, key_mask):
                models.append(value)

        return models

    def save(self, obj: DictModel):
        obj_copy = obj.copy()
        self.session[obj_copy.id] = obj_copy

    def update_many(self, specifications: Iterable[Specification], updated_fields: dict):
        keys = self.apply_specifications(specifications)

        for key in self.session:
            if re.match(key, keys):
                for field, value in updated_fields.items():
                    setattr(self.session[key].value, field, value)

    def delete(self, obj):
        del self.session[obj.id]

    def update(self, obj: DictModel):
        obj_copy = obj.copy()
        self.session[obj_copy.id] = obj_copy

    def is_modified(self, obj):
        return self.get(DictKeySpecification(obj.id)) == obj

    def refresh(self, obj):
        obj.value = self.get(DictKeySpecification(obj.id))
