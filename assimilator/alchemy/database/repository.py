from typing import Type, Union, Optional, TypeVar, Collection

from sqlalchemy import func, select, update, delete, Delete
from sqlalchemy.orm import Session, Query   # TODO: change query for alchemy 2
from sqlalchemy.inspection import inspect

from assimilator.core.patterns.error_wrapper import ErrorWrapper
from assimilator.core.database.exceptions import InvalidQueryError
from assimilator.alchemy.database.error_wrapper import AlchemyErrorWrapper
from assimilator.alchemy.database.specifications import AlchemySpecificationList
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

    def update(self, obj: Optional[AlchemyModelT] = None, *specifications, **update_values) -> None:
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

            self.session.execute(query.values(update_values).execution_options(synchronize_session=False))

        elif obj is not None:
            if obj not in self.session:
                obj = self.session.merge(obj)

            self.session.add(obj)

    def save(self, obj: Optional[AlchemyModelT] = None, **data) -> AlchemyModelT:
        if obj is None:
            for key in inspect(self.model).relationships.keys():
                foreign_data = data.get(key)
                if foreign_data is None:
                    continue

                foreign_prop = getattr(self.model, key).property
                foreign_model = foreign_prop.mapper.class_

                if not foreign_prop.uselist and isinstance(foreign_data, dict):
                    foreign_data = foreign_model(**foreign_data)

                elif foreign_prop.uselist:
                    foreign_models = (f_obj for f_obj in foreign_data if isinstance(f_obj, dict))

                    for i, f_data in enumerate(foreign_models):
                        foreign_data[i] = foreign_model(**f_data)

                data[key] = foreign_data

            obj = self.model(**data)

        self.session.add(obj)
        return obj

    def refresh(self, obj: AlchemyModelT) -> None:
        if obj not in self.session:
            obj = self.session.merge(obj)

        self.session.refresh(obj)

    def delete(self, obj: Optional[AlchemyModelT] = None, *specifications: SpecificationType) -> None:
        obj, specifications = self._check_obj_is_specification(obj, specifications)

        if specifications:
            query: Delete = self._apply_specifications(
                query=delete(self.model),
                specifications=specifications,
            )
            self.session.execute(query.execution_options(synchronize_session=False))
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
