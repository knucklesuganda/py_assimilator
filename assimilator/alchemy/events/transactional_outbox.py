from assimilator.core.events.events import Event
from assimilator.core.events.events_bus import EventProducer
from assimilator.core.database.unit_of_work import UnitOfWork
from assimilator.core.events.transactional_outbox import TransactionalOutbox


class AlchemyTransactionalOutbox(TransactionalOutbox):
    def __init__(self, event_model, producer: EventProducer, events_uow: UnitOfWork, delay: float = 10):
        super(AlchemyTransactionalOutbox, self).__init__(
            producer=producer,
            events_uow=events_uow,
            delay=delay,
        )
        self.event_model = event_model

    def get_event_data(self, event):
        return event.event_data

    def create_event_model(self, event: Event):
        return self.event_model(
            id=str(event.id),
            event_name=event.event_name,
            event_data=event.json(),
        )


__all__ = [
    'AlchemyTransactionalOutbox',
]
