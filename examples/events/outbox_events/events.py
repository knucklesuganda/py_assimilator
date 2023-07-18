from assimilator.core.events.events import Event


class OutboxEvent(Event):
    first_data: bool
    second_data: str
