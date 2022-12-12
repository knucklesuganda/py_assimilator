from assimilator.core.database.unit_of_work import UnitOfWork


class RedisUnitOfWork(UnitOfWork):
    _pipeline = None

    def begin(self):
        self._pipeline = self.repository.session.pipeline()
        self.repository.session = self._pipeline

    def rollback(self):
        self._pipeline.discard()

    def commit(self):
        self._pipeline.execute()

    def close(self):
        self._pipeline.reset()
        self._pipeline = None
