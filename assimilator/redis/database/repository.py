from typing import Type, Union, Iterable

import redis

from assimilator.core.database import SpecificationList, SpecificationType
from assimilator.redis.database import RedisModel
from assimilator.core.database.repository import BaseRepository, LazyCommand
from assimilator.internal.database.specifications import InternalSpecification, InternalSpecificationList


class RedisRepository(BaseRepository):
    def __init__(
        self,
        session: redis.Redis,
        model: Type[RedisModel],
        specifications: Type[SpecificationList] = InternalSpecificationList,
    ):
        super(RedisRepository, self).__init__(session, initial_query='', specifications=specifications)
        self.model = model

    def get(self, *specifications: InternalSpecification, lazy: bool = False, initial_query=None)\
            -> Union[LazyCommand, RedisModel]:
        key_name = self._apply_specifications(specifications, initial_query=initial_query)
        if lazy:
            return LazyCommand(lambda: self.model.from_json(self.session.get(key_name)))

        return self.model.from_json(self.session.get(key_name))

    def filter(self, *specifications: InternalSpecification, lazy: bool = False, initial_query=None)\
            -> Union[LazyCommand, Iterable['RedisModel']]:
        if lazy:
            return LazyCommand(self.filter, *specifications, lazy=False, initial_query=initial_query)

        key_name = self._apply_specifications(specifications, initial_query=initial_query)
        return [self.model.from_json(value) for value in self.session.mget(self.session.keys(key_name))]

    def save(self, obj: RedisModel):
        self.session.set(str(obj.id), obj.json(), ex=obj.expire_in)

    def delete(self, obj: RedisModel):
        self.session.delete(str(obj.id))

    def update(self, obj: RedisModel):
        self.save(obj)

    def is_modified(self, obj: RedisModel):
        return self.get(self.specifications.filter(obj.id), lazy=False) == obj

    def refresh(self, obj: RedisModel):
        fresh_obj = self.get(self.specifications.filter(obj.id), lazy=False)

        for key, value in fresh_obj.dict().items():
            setattr(obj, key, value)

    def count(self, *specifications: SpecificationType, lazy: bool = False) -> Union[LazyCommand, int]:
        if lazy:
            return LazyCommand(self.count, *specifications, lazy=False)
        elif not specifications:
            return self.session.dbsize()
        else:
            return len(self.session.keys(self._apply_specifications(specifications)))


__all__ = [
    'RedisRepository',
]
