from typing import Collection, Generic, Optional, Type, TypeVar, Union, cast, Any, Literal

from sqlalchemy import Executable, delete, func, select, update
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeMeta, Query, Session

from assimilator.alchemy.database.error_wrapper import AlchemyErrorWrapper
from assimilator.alchemy.database.model_utils import dict_to_alchemy_models, is_querying_model
from assimilator.alchemy.database.specifications.specifications import (
    AlchemySpecificationList,
)
from assimilator.core.database import LazyCommand, Repository, SpecificationType
from assimilator.core.database.exceptions import InvalidQueryError
from assimilator.core.patterns.error_wrapper import ErrorWrapper

SessionT = TypeVar("SessionT", bound=Session)
ModelT = TypeVar("ModelT", bound=DeclarativeMeta)
QueryT = TypeVar("QueryT", bound=Executable)
SpecsT = TypeVar("SpecsT", bound=Type[AlchemySpecificationList])


class AlchemyRepository(
    Repository[SessionT, ModelT, QueryT, SpecsT],
    Generic[SessionT, ModelT, QueryT, SpecsT],
):
    session: Session
    model: Type[ModelT]

    def __init__(
        self,
        session: Session,
        model: Type[ModelT],
        initial_query: Query = None,
        specifications: SpecsT = AlchemySpecificationList,
        error_wrapper: Optional[ErrorWrapper] = None,
    ):
        super().__init__(
            session=session,
            model=model,
            initial_query=initial_query if initial_query is not None else select(model),
            specifications=specifications,
            error_wrapper=error_wrapper or AlchemyErrorWrapper(),
        )

    def get(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: Query = None,
    ) -> Union[ModelT, LazyCommand[ModelT]]:
        query = self._apply_specifications(
            query=initial_query,
            specifications=specifications,
        )
        return self.session.execute(query).one()[0]

    def aggregate(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: QueryT = None,
        result_type: Literal['single', 'all'] = 'single',
    ) -> Any:
        query = self._apply_specifications(
            query=initial_query,
            specifications=specifications,
        )
        result = self.session.execute(query)

        if result_type == 'single':
            return result.one()
        elif result_type == 'all':
            return result.all()

        raise NotImplementedError("Invalid result type")

    def filter(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: Query = None,
    ) -> Union[Collection[ModelT], LazyCommand[Collection[ModelT]]]:
        query = self._apply_specifications(
            query=initial_query,
            specifications=specifications,
        )
        return [result[0] for result in self.session.execute(query)]

    def update(
        self,
        obj: Optional[ModelT] = None,
        *specifications: SpecificationType,
        **update_values,
    ) -> None:
        obj, specifications = self._check_obj_is_specification(
            obj=obj, specifications=specifications
        )

        if specifications:
            if not update_values:
                raise InvalidQueryError(
                    "You did not provide any update_values "
                    "to the update() yet provided specifications"
                )

            query = self._apply_specifications(
                query=update(self.model),
                specifications=specifications,
            )
            self.session.execute(
                query.values(update_values).execution_options(synchronize_session=False)
            )

        elif obj is not None:
            if obj not in self.session:
                obj = self.session.merge(obj)
                self.session.add(obj)

    def dict_to_models(self, data: dict) -> ModelT:
        return self.model(**dict_to_alchemy_models(data=data, model=self.model))

    def save(self, obj: Optional[ModelT] = None, **data) -> ModelT:
        if obj is None:
            obj = self.dict_to_models(data)

        self.session.add(obj)
        return obj

    def refresh(self, obj: ModelT) -> None:
        if obj not in self.session:
            obj = self.session.merge(obj)

        self.session.refresh(obj)

    def delete(
        self, obj: Optional[ModelT] = None, *specifications: SpecificationType
    ) -> None:
        obj, specifications = self._check_obj_is_specification(obj, specifications)

        if specifications:
            self.session.execute(
                self._apply_specifications(
                    query=delete(self.model),
                    specifications=specifications,
                )
            )
        elif obj is not None:
            self.session.delete(obj)

    def is_modified(self, obj: ModelT) -> bool:
        return obj in self.session and self.session.is_modified(obj)

    def count(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: Query = None,
    ) -> Union[LazyCommand[int], int]:
        primary_keys = inspect(self.model).primary_key

        if not primary_keys:
            raise InvalidQueryError(
                "Your repository model does not have any primary keys. "
                "We cannot use count()"
            )

        counter = self.get(
            *specifications,
            lazy=False,
            initial_query=initial_query
            or select(func.count(getattr(self.model, primary_keys[0].name))),
        )

        return cast(Union[LazyCommand[int], int], counter)


__all__ = [
    "AlchemyRepository",
]
