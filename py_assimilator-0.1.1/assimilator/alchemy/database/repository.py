from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Query

from assimilator.core.database import BaseRepository
from assimilator.alchemy.database.exceptions import NotFoundError


class AlchemyRepository(BaseRepository):
    def __init__(self, session, initial_query: Query = None):
        super(AlchemyRepository, self).__init__(session)
        self.initial_query = initial_query

    def get_initial_query(self):
        if self.initial_query is not None:
            return self.initial_query
        else:
            raise NotImplementedError("You must either pass the initial query "
                                      "to the constructor or define get_initial_query()")

    def _execute_query(self, query):
        return self.session.execute(query)

    def get(self, *specification, lazy=False):
        try:
            if lazy:
                return super(AlchemyRepository, self).get(*specification)
            else:
                return self._execute_query(super(AlchemyRepository, self).get(*specification)).one()[0]
        except NoResultFound as exc:
            raise NotFoundError(exc)

    def filter(self, *specifications, lazy=False):
        if lazy:
            return super(AlchemyRepository, self).filter(*specifications)
        else:
            return [result[0] for result in self._execute_query(super(AlchemyRepository, self).filter(*specifications))]

    def update(self, obj):
        """ We don't do anything, as the object is going to be updated with the obj.key = value """

    def update_many(self, specifications, updated_fields):
        self.filter(*specifications, lazy=True).update(updated_fields)

    def save(self, obj):
        self.session.add(obj)

    def refresh(self, obj):
        self.session.refresh(obj)

    def delete(self, obj):
        self.session.delete(obj)

    def is_modified(self, obj):
        return self.session.is_modified(obj)
