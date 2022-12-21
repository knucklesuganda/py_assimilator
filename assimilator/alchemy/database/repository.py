from typing import Type, Union

from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Query

from assimilator.alchemy.database.specifications import AlchemySpecificationList
from assimilator.core.database import BaseRepository, Specification, SpecificationList, LazyCommand
from assimilator.core.database.exceptions import NotFoundError


class AlchemyRepository(BaseRepository):
    def __init__(
        self,
        session,
        initial_query: Query = None,
        specifications: Type[SpecificationList] = AlchemySpecificationList,
    ):
        super(AlchemyRepository, self).__init__(
            session=session,
            initial_query=initial_query,
            specifications=specifications,
        )

    def _execute_query(self, query):
        return self.session.execute(query)

    def get(self, *specifications: Specification, lazy: bool = False, initial_query=None):
        try:
            if lazy:
                return LazyCommand(self.get, *specifications, initial_query=initial_query, lazy=False)

            query = self._apply_specifications(specifications, initial_query=initial_query)
            return self._execute_query(query).one()[0]
        except NoResultFound as exc:
            raise NotFoundError(exc)

    def filter(self, *specifications: Specification, lazy: bool = False, initial_query=None):
        if lazy:
            return LazyCommand(self.filter, *specifications, initial_query=initial_query, lazy=False)

        query = self._apply_specifications(specifications, initial_query=initial_query)
        return [result[0] for result in self._execute_query(query)]

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
        return self.get(*specifications, lazy=lazy, initial_query=select(func.count()))


__all__ = [
    'AlchemyRepository',
]
