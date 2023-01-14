from assimilator.alchemy.database.repository import AlchemyRepository
from assimilator.alchemy.database.error_wrapper import AlchemyErrorWrapper
from assimilator.core.database.unit_of_work import UnitOfWork
from assimilator.core.patterns.error_wrapper import ErrorWrapper


class AlchemyUnitOfWork(UnitOfWork):
    def __init__(self, repository: AlchemyRepository, error_wrapper: ErrorWrapper = None):
        super(AlchemyUnitOfWork, self).__init__(repository)
        self.error_wrapper = error_wrapper if error_wrapper is not None else AlchemyErrorWrapper()

    def begin(self):
        with self.error_wrapper:
            self.repository.session.begin()

    def rollback(self):
        with self.error_wrapper:
            self.repository.session.rollback()

    def close(self):
        pass

    def commit(self):
        with self.error_wrapper:
            self.repository.session.commit()


__all__ = [
    'AlchemyUnitOfWork',
]
