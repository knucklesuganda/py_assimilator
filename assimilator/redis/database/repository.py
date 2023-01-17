from typing import Type, Union, Iterable, Optional

from redis import Redis

from assimilator.redis.database import RedisModel
from assimilator.core.database.exceptions import DataLayerError, NotFoundError
from assimilator.core.patterns.error_wrapper import ErrorWrapper
from assimilator.core.database import SpecificationList, SpecificationType
from assimilator.core.database.repository import BaseRepository, LazyCommand, make_lazy
from assimilator.internal.database.specifications import InternalSpecificationList


class RedisRepository(BaseRepository):
    session: Redis

    def __init__(
        self,
        session: Redis,
        model: Type[RedisModel],
        initial_query: Optional[str] = '',
        specifications: Type[SpecificationList] = InternalSpecificationList,
        error_wrapper: Optional[ErrorWrapper] = None,
    ):
        super(RedisRepository, self).__init__(
            session=session,
            model=model,
            initial_query=initial_query,
            specifications=specifications,
        )
        self.error_wrapper = error_wrapper if not \
            error_wrapper else ErrorWrapper(default_error=DataLayerError)

    @make_lazy
    def get(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: str = None,
    ) -> Union[LazyCommand[RedisModel], RedisModel]:
        query = self._apply_specifications(
            query=self.get_initial_query(initial_query),
            specifications=specifications,
        )

        found_obj = self.session.get(query)
        if found_obj is None:
            raise NotFoundError()

        return self.model.from_json(found_obj)

    @make_lazy
    def filter(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: str = None,
    ) -> Union[LazyCommand, Iterable[RedisModel]]:


        models = [
            self.model.from_json(value)
            for value in self.session.mget(self.session.keys(key_name))
        ]

    def save(self, obj: RedisModel):
        self.session.rpush(str(obj.id), obj.json())

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
