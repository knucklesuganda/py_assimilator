from typing import Type, Union, Iterable, Optional

from redis import Redis

from assimilator.redis.database import RedisModel
from assimilator.core.database.exceptions import DataLayerError
from assimilator.core.patterns.error_wrapper import ErrorWrapper
from assimilator.core.database import SpecificationList, SpecificationType
from assimilator.core.database.repository import BaseRepository, LazyCommand, make_lazy
from assimilator.internal.database.specifications import InternalSpecification, InternalSpecificationList


class RedisRepository(BaseRepository):
    model: Type[RedisModel]

    def __init__(
        self,
        session: Redis,
        model: Type[RedisModel],
        initial_query: str = '',
        specifications: Type[SpecificationList] = InternalSpecificationList,
        error_wrapper: Optional[ErrorWrapper] = None,
    ):
        super(RedisRepository, self).__init__(
            session=session,
            model=model,
            initial_query=initial_query,
            specifications=specifications,
        )
        self.error_wrapper = error_wrapper if not error_wrapper else ErrorWrapper(default_error=DataLayerError)

    @make_lazy
    def get(
        self,
        *specifications: InternalSpecification,
        lazy: bool = False,
        initial_query: str = None,
    ) -> Union[LazyCommand, RedisModel]:
        query = self._apply_specifications(specifications, initial_query=initial_query)
        return self.model.from_json(self.session.get(query))

    @make_lazy
    def filter(
        self,
        *specifications: InternalSpecification,
        lazy: bool = False,
        initial_query: str = None,
    ) -> Union[LazyCommand, Iterable[RedisModel]]:
        key_name = self._apply_specifications(specifications, initial_query=initial_query)
        return [
            self.model.from_json(value)
            for value in self.session.mget(self.session.keys(key_name))
        ]

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

    @make_lazy
    def count(self, *specifications: SpecificationType, lazy: bool = False) -> Union[LazyCommand, int]:
        if specifications:
            return self.session.dbsize()
        return len(self.session.keys(self._apply_specifications(specifications)))


__all__ = [
    'RedisRepository',
]
