from sqlalchemy.exc import IntegrityError

from assimilator.core.database.unit_of_work import UnitOfWork
from assimilator.core.database.exceptions import InvalidQueryError


class AlchemyUnitOfWork(UnitOfWork):
    def begin(self):
        self.repository.session.begin()

    def rollback(self):
        self.repository.session.rollback()

    def close(self):
        pass

    def commit(self):
        try:
            self.repository.session.commit()
        except IntegrityError as exc:
            raise InvalidQueryError(exc)


__all__ = [
    'AlchemyUnitOfWork',
]
