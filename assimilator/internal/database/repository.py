import re
from typing import Iterable, Any, Type

from pydantic import BaseModel

from assimilator.core.database import BaseRepository, Specification
from assimilator.core.database.exceptions import NotFoundError
from assimilator.internal.database.specifications import DictSpecification


class DictModel(BaseModel):
    key: str
    value: Any


class DictRepository(BaseRepository):
    def __init__(self, session: dict, model: Type[DictModel] = DictModel):
        super(DictRepository, self).__init__(session)
        self.model = model

    def get_initial_query(self):
        return ''

    def get(self, *specifications: DictSpecification, lazy: bool = False):
        try:
            key = super(DictRepository, self).get(*specifications, lazy=lazy)
            value = self.session[key]
            return self.model(value=value, key=key)
        except (KeyError, TypeError) as exc:
            raise NotFoundError(exc)

    def filter(self, *specifications: DictSpecification, lazy: bool = False):
        models = []
        key_mask = self.apply_specifications(specifications)

        for key, value in self.session.items():
            if re.match(key, key_mask):
                models.append(self.model(value=value, key=key))

        return models

    def save(self, obj: DictModel):
        self.session[obj.key] = obj.value

    def update_many(self, specifications: Iterable[Specification], updated_fields: dict):
        keys = self.apply_specifications(specifications)

        for key in self.session:
            if re.match(key, keys):
                for field, value in updated_fields.items():
                    setattr(self.session[key].value, field, value)

    def delete(self, obj):
        del self.session[obj.key]

    def update(self, obj):
        self.session[obj.key] = obj.value

    def is_modified(self, obj):
        return self.session[obj.key] == obj

    def refresh(self, obj):
        obj.value = self.session[obj.key]
