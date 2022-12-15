from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from assimilator.core.patterns.mixins import JSONParsedMixin


class Event(JSONParsedMixin, BaseModel):
    id: int
    event_name: str
    event_date: datetime = Field(default_factory=datetime.now)


class ExternalEvent(Event):
    """ The event type is unknown, so all the fields are in data """
    data: Any


class AckEvent(Event):
    acknowledged: bool = False
