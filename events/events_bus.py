from events.events import Event


class EventBus:
    def __init__(self, event_storage):
        self.event_storage = event_storage

    def emit(self, event: Event):
        raise NotImplementedError("emit() is not implemented")

    def consume(self):
        raise NotImplementedError()
