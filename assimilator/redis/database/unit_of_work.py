from assimilator.core.database.unit_of_work import UnitOfWork


class RedisUnitOfWork(UnitOfWork):
    _saved_session = None

    def begin(self):
        self._saved_session = self.repository.session
        self.repository.session = self.repository.session.pipeline()

    def rollback(self):
        self.repository.session.discard()

    def commit(self):
        self.repository.session.execute()

    def close(self):
        self.repository.session.reset()
        self.repository.session = self._saved_session
        self._saved_session = None
