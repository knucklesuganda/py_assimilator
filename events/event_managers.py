from events.events import Event


class EventManager:
    def __init__(self, event_storage):
        self.event_storage = event_storage

    def emit(self, event: Event):
        raise NotImplementedError("emit() is not implemented")

    def consume(self):
        raise NotImplementedError()
