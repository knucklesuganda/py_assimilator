import json
from typing import Iterable, Type

import redis

from assimilator.core.database.repository import BaseRepository
from assimilator.core.database.specifications import Specification
from assimilator.redis.database.models import RedisModel
from assimilator.redis.database.specifications import FilterSpecification


class RedisLazyCommand:
    def __init__(self, command: callable, *args):
        self.command = command
        self.args = args

    def __call__(self):
        return self.command(*self.args)


class RedisRepository(BaseRepository):
    def __init__(
        self,
        session: redis.Redis,
        model: Type[RedisModel],
        lazy_command_cls: Type[RedisLazyCommand] = RedisLazyCommand,
    ):
        super(RedisRepository, self).__init__(session)
        self.lazy_command_cls = lazy_command_cls
        self.model = model

    def get_initial_query(self):
        """
        Redis specifications get a str filter and return a new one.
        That is why the initial_query is an empty str.
        """
        return ''

    def get(self, *specifications: Specification, lazy: bool = False):
        key_name = self._apply_specifications(specifications)

        if lazy:
            return self.lazy_command_cls(self.session.get, key_name)
        else:
            return self.model.from_json(self.session.get(key_name))

    def filter(self, *specifications: Specification, lazy: bool = False):
        key_name = self._apply_specifications(specifications)

        if lazy:
            return self.lazy_command_cls(self.session.keys, key_name)

        keys = self.session.keys(key_name)
        return [self.model.from_json(value) for value in self.session.mget(*keys)]

    def save(self, obj: RedisModel):
        self.session.set(str(obj.id), obj.json())

    def delete(self, obj: RedisModel):
        self.session.delete(str(obj.id))

    def update(self, obj: RedisModel):
        self.save(obj)

    def is_modified(self, obj: RedisModel):
        return self.get(FilterSpecification(obj.id), lazy=False) == obj

    def refresh(self, obj: RedisModel):
        fresh_obj = self.get(FilterSpecification(obj.id), lazy=False)

        for key, value in fresh_obj.dict().items():
            setattr(obj, key, value)
