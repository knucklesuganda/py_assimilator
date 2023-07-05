from typing import Iterable

from assimilator.core.events.events import Event
from assimilator.core.events.events_bus import EventConsumer, EventProducer


class InternalEventConsumer(EventConsumer):
    """ Consumer for internal events """


class InternalEventProducer(EventProducer):
    def __init__(self, consumer: EventConsumer):
        self.consumer = consumer

    def produce(self, event: Event):
        self.consumer.consume(event)

    def mass_produce(self, events: Iterable[Event]) -> None:
        for event in events:
            self.consumer.consume(event)


__all__ = [
    'InternalEventConsumer',
    'InternalEventProducer',
]
