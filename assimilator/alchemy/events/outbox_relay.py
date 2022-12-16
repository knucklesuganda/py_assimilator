from sqlalchemy import Column, BigInteger, Text, DateTime

from assimilator.core.events import Event
from assimilator.core.database.unit_of_work import UnitOfWork
from assimilator.core.events import OutboxRelay
from assimilator.core.events.events_bus import EventBus


def create_outbox_event_model(Base):
    class OutboxEvent(Base):
        id = Column(BigInteger(), primary_key=True)
        event_data = Column(Text())
        event_date = Column(DateTime(timezone=True))

        def __init__(self, event: Event, *args, **kwargs):
            super(OutboxEvent, self).__init__(
                event_data=event.json(),
                event_date=event.event_date,
                *args,
                **kwargs,
            )

    return OutboxEvent


class AlchemyOutboxRelay(OutboxRelay):
    def __init__(self, outbox_event_model, uow: UnitOfWork, event_bus: EventBus):
        super(AlchemyOutboxRelay, self).__init__(uow=uow, event_bus=event_bus)
        self.outbox_event_model = outbox_event_model

    def start(self):
        while True:
            with self.uow:
                events = self.uow.repository.filter()

                for event in events:
                    self.event_bus.produce(event)

                self.acknowledge(events)
                self.uow.commit()

            self.delay_function()

    def delay_function(self):
        raise NotImplementedError("delay_function() is not implemented")

    def acknowledge(self, events):
        for event in events:
            self.uow.repository.delete(event)
