from sqlalchemy import Column, BigInteger, Text, DateTime

from assimilator.core.events import Event
from assimilator.core.database.unit_of_work import UnitOfWork
from assimilator.core.events import OutboxRelay
from assimilator.core.events.events_bus import EventBus


def create_outbox_event_model(tablename: str, Base):
    class OutboxEvent(Base):
        __tablename__ = tablename

        id = Column(BigInteger(), primary_key=True)
        event_data = Column(Text())
        event_date = Column(DateTime(timezone=True))

        def __init__(self, event: Event, *args, **kwargs):
            super(OutboxEvent, self).__init__(
                *args,
                id=event.id,
                event_data=event.json(),
                event_date=event.event_date,
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
                objects = self.uow.repository.filter()

                for event in objects:
                    self.event_bus.produce(event.event)
                    self.acknowledge(event.event)
                self.uow.commit()

            self.delay_function()

    def delay_function(self):
        raise NotImplementedError("delay_function() is not implemented")

    def acknowledge(self, events):
        for event in events:
            self.uow.repository.delete(event.event)
