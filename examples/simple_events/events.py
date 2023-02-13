from assimilator.core.events import Event


class RecordCreated(Event):
    record_name: str
    event_name = "record_created"
