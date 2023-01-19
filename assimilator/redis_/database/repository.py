from typing import Type, Union, Optional, TypeVar, Collection

from redis import Redis
from redis.client import Pipeline

from assimilator.redis_.database import RedisModel
from assimilator.core.patterns.error_wrapper import ErrorWrapper
from assimilator.core.database import (
    SpecificationList, SpecificationType, Repository, LazyCommand, make_lazy,
)
from assimilator.internal.database.specifications import InternalSpecificationList
from assimilator.core.database.exceptions import DataLayerError, NotFoundError, InvalidQueryError

RedisModelT = TypeVar("RedisModelT", bound=RedisModel)


class RedisRepository(Repository):
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
        use_double_filter: bool = True,
    ):
        super(RedisRepository, self).__init__(
            session=session,
            model=model,
            initial_query=initial_query,
            specifications=specifications,
            error_wrapper=error_wrapper or ErrorWrapper(
                default_error=DataLayerError,
                skipped_errors=(NotFoundError,)
            )
        )
        self.transaction = session
        self.use_double_specifications = use_double_filter

    @make_lazy
    def get(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: Optional[str] = None,
    ) -> Union[LazyCommand[RedisModelT], RedisModelT]:
        query = self._apply_specifications(
            query=self.get_initial_query(initial_query),
            specifications=specifications,
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
        if self.use_double_specifications and specifications:
            key_name = self._apply_specifications(
                query=self.get_initial_query(initial_query),
                specifications=specifications,
            ) or "*"
        else:
            key_name = "*"

        key_name = key_name or "*"

        models = self.session.mget(self.session.keys(key_name))
        return list(self._apply_specifications(specifications=specifications, query=[
            self.model.from_json(value) for value in models
        ]))

    def save(self, obj: Optional[RedisModelT] = None, **obj_data) -> RedisModelT:
        if obj is None:
            obj = self.model(**obj_data)

        self.transaction.set(
            name=obj.id,
            value=obj.json(),
            ex=obj.expire_in,
            px=obj.expire_in_px,
            nx=obj.only_create,
            xx=obj.only_update,
            keepttl=obj.keep_ttl,
        )
        return obj

    def delete(self, obj: Optional[RedisModelT] = None, *specifications: SpecificationType) -> None:
        obj, specifications = self._check_obj_is_specification(obj, specifications)

        if specifications:
            models = self.filter(*specifications)
            self.transaction.delete(*[str(model.id) for model in models])
        elif obj is not None:
            self.transaction.delete(obj.id)

    def update(
        self,
        obj: Optional[RedisModelT] = None,
        *specifications: SpecificationType,
        **update_values,
    ) -> None:
        obj, specifications = self._check_obj_is_specification(obj, specifications)

        if specifications:
            if not update_values:
                raise InvalidQueryError(
                    "You did not provide any update_values "
                    "to the update() yet provided specifications"
                )

            models = self.filter(*specifications, lazy=False)
            updated_models = {}

            for model in models:
                model.__dict__.update(update_values)
                updated_models = {model.id: model}

            self.transaction.mset(updated_models)

        elif obj is not None:
            obj.only_update = True
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

        filter_query = self._apply_specifications(
            query=self.get_initial_query(),
            specifications=specifications,
        )
        return len(self.session.keys(filter_query))


__all__ = [
    'RedisRepository',
]
