from database.alchemy.specifications import ValueInSpecification
from database.base.unit_of_work import UnitOfWork
from events.alchemy.models import EventModel
from events.alchemy.specifications import EventNotAckSpecification
from events.events_bus import EventBus
from events.outbox_relay import OutboxRelay


class AlchemyOutboxRelay(OutboxRelay):
    def __init__(self, model: EventModel, uow: UnitOfWork, event_bus: EventBus):
        self.model = model
        super(AlchemyOutboxRelay, self).__init__(uow=uow, event_bus=event_bus)

    def start(self):
        while True:
            with self.uow:
                events = self.uow.repository.filter(EventNotAckSpecification(self.model.acknowledged_field))

                for event in events:
                    self.event_bus.emit(event)

                self.acknowledge(events)
                self.uow.commit()

            self.delay_function()

    def delay_function(self):
        raise NotImplementedError("delay function is not implemented")

    def acknowledge(self, events):
        self.uow.repository.update_many(
            specifications=[ValueInSpecification(field=self.model, values=events)],
            updated_fields={self.model.acknowledged_field: True},
        )
