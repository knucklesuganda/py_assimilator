from typing import Union, Optional, Collection, Type, TypeVar, final

from pymongo import MongoClient

from assimilator.core.database import make_lazy
from assimilator.mongo.database.models import MongoModel
from assimilator.core.patterns import LazyCommand, ErrorWrapper
from assimilator.mongo.database.error_wrapper import MongoErrorWrapper
from assimilator.core.database import Repository, SpecificationType, SpecificationList, NotFoundError
from assimilator.mongo.database.specifications.specifications import MongoSpecificationList

ModelT = TypeVar("ModelT", bound=MongoModel)


class MongoRepository(Repository):
    session: MongoClient
    model: Type[MongoModel]

    def __init__(
        self,
        session: MongoClient,
        model: Type[MongoModel],
        database: str,
        specifications: Type[SpecificationList] = MongoSpecificationList,
        initial_query: Optional[dict] = None,
        error_wrapper: Optional[ErrorWrapper] = None,
    ):
        super(MongoRepository, self).__init__(
            session=session,
            model=model,
            initial_query=initial_query or {},
            specifications=specifications,
            error_wrapper=error_wrapper or MongoErrorWrapper(),
        )
        self.database = database

    @final
    @property
    def _collection(self):
        return self.session[self.database][self.model.get_collection()]

    def get(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: dict = None,
    ):
        query = self._apply_specifications(
            query=self.get_initial_query(initial_query),
            specifications=specifications,
        )

        data = self._collection.find_one(**query)

        if data is None:
            raise NotFoundError()

        return self.model(**data)

    def filter(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: dict = None
    ) -> Union[Collection[ModelT], LazyCommand[Collection[ModelT]]]:
        query = self._apply_specifications(
            query=self.get_initial_query(initial_query),
            specifications=specifications,
        )
        return [self.model(**data) for data in self._collection.find(**query)]

    def save(self, obj: Optional[ModelT] = None, **obj_data) -> ModelT:
        if obj is None:
            obj = self.model(**obj_data)

        self._collection.insert_one(obj.dict())
        return obj

    def delete(self, obj: Optional[ModelT] = None, *specifications: SpecificationType) -> None:
        obj, specifications = self._check_obj_is_specification(obj, specifications)

        if specifications:
            self._collection.delete_many(**self._apply_specifications(
                query=self.get_initial_query(),
                specifications=specifications,
            ))
        elif obj is not None:
            self._collection.delete_one(obj.dict())

    def update(
        self,
        obj: Optional[ModelT] = None,
        *specifications: SpecificationType,
        **update_values,
    ) -> None:
        obj, specifications = self._check_obj_is_specification(obj, specifications)

        if specifications:
            self._collection.update_many(
                filter=self._apply_specifications(
                    query=self.get_initial_query(),
                    specifications=specifications,
                ),
                update=update_values,
                upsert=self.model.upsert,
            )
        elif obj is not None:
            self._collection.update_one(
                {"_id": obj.id},
                update={'$set': obj.dict()},
                upsert=obj.upsert,
            )

    def is_modified(self, obj: ModelT) -> bool:
        return self.get(self.specs.filter(id=obj.id)) == obj

    def refresh(self, obj: ModelT) -> None:
        fresh_obj = self.get(self.specs.filter(id=obj.id))
        obj.__dict__.update(fresh_obj.__dict__)

    def count(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: Optional[dict] = None,
    ) -> Union[LazyCommand[int], int]:
        return self._collection.count_documents(
            filter=self._apply_specifications(
                query=self.get_initial_query(initial_query),
                specifications=specifications,
            ),
        )


__all__ = ['MongoRepository']
