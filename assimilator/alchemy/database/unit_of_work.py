from assimilator.alchemy.database.repository import AlchemyRepository
from assimilator.alchemy.database.error_wrapper import AlchemyErrorWrapper
from assimilator.core.database.unit_of_work import UnitOfWork
from assimilator.core.patterns.error_wrapper import ErrorWrapper


class AlchemyUnitOfWork(UnitOfWork):
    def __init__(self, repository: AlchemyRepository, error_wrapper: ErrorWrapper = None):
        super(AlchemyUnitOfWork, self).__init__(
            repository=repository,
            error_wrapper=error_wrapper or AlchemyErrorWrapper(),
        )

    def begin(self):
        self.repository.session.begin()

    def rollback(self):
        self.repository.session.rollback()

    def close(self):
        pass

    def commit(self):
        self.repository.session.commit()


__all__ = [
    'AlchemyUnitOfWork',
]
