from datetime import datetime
from typing import Any

from pydantic import Field

from core.database.models import BaseModel


class Event(BaseModel):
    event_name: str = Field(allow_mutation=False)
    event_date: datetime = Field(default_factory=datetime.now)

    class Config:
        validate_assignment = True


class ExternalEvent(Event):
    """ The event type is unknown, so all the fields are in data """
    data: Any


class AckEvent(Event):
    acknowledged: bool = False


__all__ = [
    'Event',
    'ExternalEvent',
    'AckEvent',
]
