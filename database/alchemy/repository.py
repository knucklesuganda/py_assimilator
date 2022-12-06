from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Query

from database.base.repository import BaseRepository
from database.alchemy.exceptions import NotFoundError


class AlchemyRepository(BaseRepository):
    def __init__(self, session, lazy: bool = False, initial_query: Query = None):
        super(AlchemyRepository, self).__init__(session)
        self.lazy = lazy
        self.initial_query = initial_query

    def get_initial_query(self):
        if self.initial_query is not None:
            return self.initial_query
        else:
            raise NotImplementedError("You must either pass the initial query "
                                      "to the constructor or define get_initial_query()")

    def _execute_query(self, query):
        return self.session.execute(query)

    def get(self, *specification):
        try:
            if self.lazy:
                return super(AlchemyRepository, self).get(*specification)
            else:
                return self._execute_query(super(AlchemyRepository, self).get(*specification)).one()[0]
        except NoResultFound as exc:
            raise NotFoundError(exc)

    def filter(self, *specifications):
        if self.lazy:
            return super(AlchemyRepository, self).filter(*specifications)
        else:
            return [result[0] for result in self._execute_query(super(AlchemyRepository, self).filter(*specifications))]

    def save(self, obj):
        self.session.add(obj)

    def refresh(self, obj):
        self.session.refresh(obj)

    def delete(self, obj):
        self.session.delete(obj)

    def is_modified(self, obj):
        return self.session.is_modified(obj)
