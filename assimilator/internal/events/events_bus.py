from assimilator.core.events.events import Event
from assimilator.core.events.events_bus import EventConsumer, EventProducer


class InternalEventConsumer(EventConsumer):
    def __init__(self, event_storage: list):
        self.event_storage = event_storage

    def close(self):
        pass

    def start(self):
        pass

    def consume(self):
        yield self.event_storage.pop()


class InternalEventProducer(EventProducer):
    def __init__(self, event_storage: list):
        self.event_storage = event_storage

    def produce(self, event: Event):
        self.event_storage.append(event)

    def start(self):
        pass

    def close(self):
        pass


__all__ = [
    'InternalEventConsumer',
    'InternalEventProducer',
]
