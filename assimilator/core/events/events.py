from typing import Any

from assimilator.core.database.models import BaseModel


class Event(BaseModel):
    event_name: str

    class Config:
        validate_assignment = True


class ExternalEvent(Event):
    """ The event type is unknown, so all the fields are in data. """
    data: Any


class AckEvent(Event):
    acknowledged: bool = False


__all__ = [
    'Event',
    'ExternalEvent',
    'AckEvent',
]
