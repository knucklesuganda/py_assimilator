from assimilator.alchemy.database.repository import AlchemyRepository


class AlchemyOutboxRepository(AlchemyRepository):
    def __init__(self, event_model, session, initial_query=None):
        super(AlchemyOutboxRepository, self).__init__(session, initial_query)
        self.event_model = event_model

    def save(self, obj):
        super(AlchemyOutboxRepository, self).save(obj)
        super(AlchemyOutboxRepository, self).save(self.event_model(obj.outbox_event))
