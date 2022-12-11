from assimilator.core.events import Event
from assimilator.core.events.events_bus import EventConsumer, EventProducer


class InternalEventConsumer(EventConsumer):
    def __init__(self, event_storage: list, listeners: dict):
        self.event_storage = event_storage
        self.listeners = listeners

    def close(self):
        pass

    def start(self):
        pass

    def consume(self):
        for _ in range(len(self.event_storage)):
            event = self.event_storage.pop()

            for listener in self.listeners:
                listener(event)


class InternalEventProducer(EventProducer):
    def __init__(self, event_storage: list):
        self.event_storage = event_storage

    def produce(self, event: Event):
        self.event_storage.append(event)

    def start(self):
        pass

    def close(self):
        pass
