from datetime import datetime
from typing import Any

from pydantic import Field

from core.database.models import BaseModel


class Event(BaseModel):
    id: int
    event_name: str
    event_date: datetime = Field(default_factory=datetime.now)


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
