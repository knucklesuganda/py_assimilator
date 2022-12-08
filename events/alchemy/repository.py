from typing import Type

from database.alchemy.repository import AlchemyRepository
from events.alchemy.models import EventModel


class AlchemyOutboxRepository(AlchemyRepository):
    def __init__(self, event_model: Type[EventModel], session, initial_query=None):
        super(AlchemyOutboxRepository, self).__init__(session, initial_query)
        self.event_model = event_model

    def save(self, obj):
        super(AlchemyOutboxRepository, self).save(obj)
        super(AlchemyOutboxRepository, self).save(self.event_model(obj))
