from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Query

from assimilator.core.database import BaseRepository, Specification
from assimilator.core.database.exceptions import NotFoundError


class AlchemyRepository(BaseRepository):
    def __init__(self, session, initial_query: Query = None):
        super(AlchemyRepository, self).__init__(session=session, initial_query=initial_query)

    def _execute_query(self, query):
        return self.session.execute(query)

    def get(self, *specifications: Specification, lazy=False):
        try:
            applied_specifications = self._apply_specifications(specifications)
            if lazy:
                return applied_specifications

            return self._execute_query(applied_specifications).one()[0]

        except NoResultFound as exc:
            raise NotFoundError(exc)

    def filter(self, *specifications: Specification, lazy=False):
        applied_specifications = self._apply_specifications(specifications)
        if lazy:
            return applied_specifications

        return [result[0] for result in self._execute_query(applied_specifications)]

    def update(self, obj):
        """ We don't do anything, as the object is going to be updated with the obj.key = value """

    def save(self, obj):
        self.session.add(obj)

    def refresh(self, obj):
        self.session.refresh(obj)

    def delete(self, obj):
        self.session.delete(obj)

    def is_modified(self, obj):
        return self.session.is_modified(obj)
