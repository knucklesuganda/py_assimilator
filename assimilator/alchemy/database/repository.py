from typing import Type, Union, Optional, TypeVar, Collection

from sqlalchemy import func, select, update, delete
from sqlalchemy.orm import Session, Query
from sqlalchemy.inspection import inspect

from assimilator.alchemy.database.model_utils import dict_to_alchemy_models
from assimilator.core.patterns.error_wrapper import ErrorWrapper
from assimilator.core.database.exceptions import InvalidQueryError
from assimilator.alchemy.database.error_wrapper import AlchemyErrorWrapper
from assimilator.alchemy.database.specifications.specifications import AlchemySpecificationList
from assimilator.core.database import Repository, LazyCommand, SpecificationType


AlchemyModelT = TypeVar("AlchemyModelT")


class AlchemyRepository(Repository):
    session: Session
    model: Type[AlchemyModelT]

    def __init__(
        self,
        session: Session,
        model: Type[AlchemyModelT],
        initial_query: Query = None,
        specifications: Type[AlchemySpecificationList] = AlchemySpecificationList,
        error_wrapper: Optional[ErrorWrapper] = None,
    ):
        super(AlchemyRepository, self).__init__(
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
    ) -> Union[AlchemyModelT, LazyCommand[AlchemyModelT]]:
        query = self._apply_specifications(
            query=initial_query,
            specifications=specifications,
        )
        return self.session.execute(query).one()[0]

    def filter(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: Query = None,
    ) -> Union[Collection[AlchemyModelT], LazyCommand[Collection[AlchemyModelT]]]:
        query = self._apply_specifications(
            query=initial_query,
            specifications=specifications,
        )
        return [result[0] for result in self.session.execute(query)]

    def update(
        self,
        obj: Optional[AlchemyModelT] = None,
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

    def dict_to_models(self, data: dict) -> AlchemyModelT:
        return self.model(**dict_to_alchemy_models(data=data, model=self.model))

    def save(self, obj: Optional[AlchemyModelT] = None, **data) -> AlchemyModelT:
        if obj is None:
            obj = self.dict_to_models(data)

        self.session.add(obj)
        return obj

    def refresh(self, obj: AlchemyModelT) -> None:
        if obj not in self.session:
            obj = self.session.merge(obj)

        self.session.refresh(obj)

    def delete(self, obj: Optional[AlchemyModelT] = None, *specifications: SpecificationType) -> None:
        obj, specifications = self._check_obj_is_specification(obj, specifications)

        if specifications:
            self.session.execute(self._apply_specifications(
                query=delete(self.model),
                specifications=specifications,
            ))
        elif obj is not None:
            self.session.delete(obj)

    def is_modified(self, obj: AlchemyModelT) -> bool:
        return obj in self.session and self.session.is_modified(obj)

    def count(
        self,
        *specifications: SpecificationType,
        lazy: bool = False,
        initial_query: Query = None
    ) -> Union[LazyCommand[int], int]:
        primary_keys = inspect(self.model).primary_key

        if not primary_keys:
            raise InvalidQueryError(
                "Your repository model does not have any primary keys. We cannot use count()"
            )

        return self.get(
            *specifications,
            lazy=False,
            initial_query=initial_query or select(func.count(getattr(self.model, primary_keys[0].name))),
        )


__all__ = [
    'AlchemyRepository',
]
