from datetime import datetime

from pydantic import BaseModel, Field


class Event(BaseModel):
    id: int
    event_name: str
    event_date: datetime = Field(default_factory=datetime.now)


class AckEvent(Event):
    acknowledged: bool = False
