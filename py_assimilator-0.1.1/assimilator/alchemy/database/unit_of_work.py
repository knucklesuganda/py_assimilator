from sqlalchemy.exc import IntegrityError

from assimilator.core.database.unit_of_work import UnitOfWork
from assimilator.alchemy.database.exceptions import InvalidQueryError


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
        except IntegrityError as exc:
            raise InvalidQueryError(
                statement=exc.statement,
                params=exc.params,
                orig=exc.orig,
                hide_parameters=exc.hide_parameters,
                connection_invalidated=exc.connection_invalidated,
                code=exc.code,
                ismulti=exc.ismulti,
            )
