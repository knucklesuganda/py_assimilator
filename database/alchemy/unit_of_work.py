from sqlalchemy import exc

from database.base.unit_of_work import UnitOfWork
from database.alchemy.exceptions import InvalidQueryError


class AlchemyUnitOfWork(UnitOfWork):
    def begin(self):
        self.repository.session.begin()

    def rollback(self):
        self.repository.session.rollback()

    def close(self):
        self.repository.session.close()

    def commit(self):
        try:
            self.repository.session.commit()
        except exc.IntegrityError:
            raise InvalidQueryError()
