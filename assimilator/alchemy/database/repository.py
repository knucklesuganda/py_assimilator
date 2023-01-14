from typing import Type, Union

from sqlalchemy import func, select, Table
from sqlalchemy.orm import Session, Query
from sqlalchemy.inspection import inspect

from assimilator.alchemy.database.error_wrapper import AlchemyErrorWrapper
from assimilator.core.database.exceptions import InvalidQueryError
from assimilator.alchemy.database.specifications import AlchemySpecificationList
from assimilator.core.database import BaseRepository, Specification, \
    SpecificationList, LazyCommand, SpecificationType
from assimilator.core.patterns.error_wrapper import ErrorWrapper


class AlchemyRepository(BaseRepository):
    def __init__(
        self,
        session: Session,
        model: Type['Table'],
        initial_query: Query = None,
        specifications: Type[SpecificationList] = AlchemySpecificationList,
        error_wrapper: ErrorWrapper = None,
    ):
        super(AlchemyRepository, self).__init__(
            session=session,
            model=model,
            initial_query=initial_query if initial_query is not None else select(model),
            specifications=specifications,
        )
        self.error_wrapper = error_wrapper if error_wrapper is not None else AlchemyErrorWrapper()

    def get(self, *specifications: SpecificationType, lazy: bool = False, initial_query=None):
        with self.error_wrapper:
            if lazy:
                return LazyCommand(self.get, *specifications, initial_query=initial_query, lazy=False)

            query = self._apply_specifications(specifications, initial_query=initial_query)
            return self.session.execute(query).one()[0]

    def filter(self, *specifications: Specification, lazy: bool = False, initial_query=None):
        with self.error_wrapper:
            if lazy:
                return LazyCommand(self.filter, *specifications, initial_query=initial_query, lazy=False)

            query = self._apply_specifications(specifications, initial_query=initial_query)
            return [result[0] for result in self.session.execute(query)]

    def update(self, obj):
        """ We don't do anything, as the object is going to be updated with the obj.key = value """

    def save(self, obj):
        self.session.add(obj)

    def refresh(self, obj):
        self.session.refresh(obj)

    def delete(self, obj):
        self.session.delete(obj)

    def is_modified(self, obj) -> bool:
        return self.session.is_modified(obj)

    def count(self, *specifications, lazy: bool = False) -> Union[LazyCommand, int]:
        with self.error_wrapper:
            primary_keys = inspect(self.model).primary_key

            if not primary_keys:
                raise InvalidQueryError("Your repository model does not have any primary keys. We cannot use count()")

            return self.get(
                *specifications,
                lazy=lazy,
                initial_query=select(func.count(getattr(self.model, primary_keys[0].name))),
            )


__all__ = [
    'AlchemyRepository',
]
