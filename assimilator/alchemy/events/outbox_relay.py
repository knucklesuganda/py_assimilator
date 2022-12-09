from sqlalchemy import Column, BigInteger, Text, DateTime, func

from assimilator.events.events import Event
from assimilator.database.unit_of_work import UnitOfWork
from assimilator.events.outbox_relay import OutboxRelay
from assimilator.events.events_bus import EventBus


def create_outbox_event_model(Base):
    class OutboxEvent(Base):
        id = Column(BigInteger())
        event_data = Column(Text())
        event_date = Column(DateTime(timezone=True), server_default=func.now())

        def __init__(self, event: Event, *args, **kwargs):
            super(OutboxEvent, self).__init__(event_data=event.json(), *args, **kwargs)

    return OutboxEvent


class AlchemyOutboxRelay(OutboxRelay):
    def __init__(self, outbox_event_model, uow: UnitOfWork, event_bus: EventBus):
        self.outbox_event_model = outbox_event_model
        super(AlchemyOutboxRelay, self).__init__(uow=uow, event_bus=event_bus)

    def start(self):
        while True:
            with self.uow:
                events = self.uow.repository.filter()

                for event in events:
                    self.event_bus.emit(event)

                self.acknowledge(events)
                self.uow.commit()

            self.delay_function()

    def delay_function(self):
        raise NotImplementedError("delay function is not implemented")

    def acknowledge(self, events):
        for event in events:
            self.uow.repository.delete(event)
