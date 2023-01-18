from typing import Type, Union, Optional, TypeVar, Collection

from redis import Redis
from redis.client import Pipeline

from assimilator.redis_.database import RedisModel
from assimilator.core.database.exceptions import DataLayerError, NotFoundError
from assimilator.core.patterns.error_wrapper import ErrorWrapper
from assimilator.core.database import (
    SpecificationList,
    SpecificationType,
    SpecificationSplitMixin,
    BaseRepository,
    LazyCommand,
    make_lazy,
)
from assimilator.internal.database.specifications import InternalSpecificationList, internal_filter

RedisModelT = TypeVar("RedisModelT", bound=RedisModel)


class RedisRepository(SpecificationSplitMixin, BaseRepository):
    session: Redis
    transaction: Union[Pipeline, Redis]
    model: Type[RedisModelT]

    def __init__(
        self,
        session: Redis,
        model: Type[RedisModelT],
        initial_query: Optional[str] = '',
        specifications: Type[SpecificationList] = InternalSpecificationList,
        error_wrapper: Optional[ErrorWrapper] = None,
    ):
        super(RedisRepository, self).__init__(
            session=session,
            model=model,
            initial_query=initial_query,
            specifications=specifications,
            error_wrapper=error_wrapper or ErrorWrapper(default_error=DataLayerError)
        )
        self.transaction = session

    def _is_before_specification(self, specification: SpecificationType) -> bool:
        return True

    @make_lazy
    def get(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: Optional[str] = None,
    ) -> Union[LazyCommand[RedisModelT], RedisModelT]:
        before_specs, _ = self._split_specifications(specifications, no_after_specs=True)

        query = self._apply_specifications(
            query=self.get_initial_query(initial_query),
            specifications=before_specs,
        )

        found_obj = self.session.get(query)
        if found_obj is None:
            raise NotFoundError(f"Redis model was not found")

        return self.model.from_json(found_obj)

    @make_lazy
    def filter(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: Optional[str] = None,
    ) -> Union[LazyCommand[Collection[RedisModelT]], Collection[RedisModelT]]:
        if not specifications:
            return [
                self.model.from_json(value)
                for value in self.session.mget(self.session.keys("*"))
            ]

        before_specs, after_specs = self._split_specifications(specifications)

        if before_specs:
            key_name = self._apply_specifications(
                query=self.get_initial_query(initial_query),
                specifications=before_specs,
            )
        else:
            key_name = "*"

        models = [
            self.model.from_json(value)
            for value in self.session.mget(self.session.keys(key_name))
        ]
        return self._apply_specifications(query=models, specifications=after_specs)

    def save(self, obj: RedisModelT) -> None:
        self.transaction.set(
            name=obj.id,
            value=obj.json(),
            ex=obj.expire_in,
            px=obj.expire_in_px,
            nx=obj.only_create,
            xx=obj.only_update,
            keepttl=obj.keep_ttl,
        )

    def delete(self, obj: RedisModelT) -> None:
        self.transaction.delete(obj.id)

    def update(self, obj: RedisModelT) -> None:
        self.save(obj)

    def is_modified(self, obj: RedisModelT) -> None:
        return self.get(self.specifications.filter(obj.id), lazy=False) == obj

    def refresh(self, obj: RedisModelT) -> None:
        fresh_obj = self.get(self.specifications.filter(obj.id), lazy=False)

        for key, value in fresh_obj.dict().items():
            setattr(obj, key, value)

    @make_lazy
    def count(self, *specifications: SpecificationType, lazy: bool = False) -> Union[LazyCommand[int], int]:
        if specifications:
            return self.session.dbsize()

        before_specs, _ = self._split_specifications(specifications, no_after_specs=True)
        filter_query = self._apply_specifications(
            query=self.get_initial_query(),
            specifications=before_specs,
        )
        return len(self.session.keys(filter_query))


__all__ = [
    'RedisRepository',
]
