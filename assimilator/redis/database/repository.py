from typing import Type

import redis

from assimilator.core.database.repository import BaseRepository, LazyCommand
from assimilator.internal.database.specifications import key_specification, InternalSpecification
from assimilator.redis.database import RedisModel


class RedisRepository(BaseRepository):
    def __init__(self, session: redis.Redis, model: Type[RedisModel]):
        super(RedisRepository, self).__init__(session, initial_query='')
        self.model = model

    def get(self, *specifications: InternalSpecification, lazy: bool = False):
        key_name = self._apply_specifications(specifications)
        if lazy:
            return LazyCommand(self.session.get, key_name)
        return self.session.get(key_name)

    def filter(self, *specifications: InternalSpecification, lazy: bool = False):
        key_name = self._apply_specifications(specifications)
        if lazy:
            return LazyCommand(self.session.keys, key_name)

        return [self.model.from_json(value) for value in self.session.mget(self.session.keys(key_name))]

    def save(self, obj: RedisModel):
        self.session.set(str(obj.id), obj.json())

    def delete(self, obj: RedisModel):
        self.session.delete(str(obj.id))

    def update(self, obj: RedisModel):
        self.save(obj)

    def is_modified(self, obj: RedisModel):
        return self.get(key_specification(obj.id), lazy=False) == obj

    def refresh(self, obj: RedisModel):
        fresh_obj = self.get(key_specification(obj.id), lazy=False)

        for key, value in fresh_obj.dict().items():
            setattr(obj, key, value)
