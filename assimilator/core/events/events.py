from abc import ABC
from typing import Any, Optional

from pydantic import Field

from assimilator.core.database.models import BaseModel


class Event(BaseModel):
    event_name: Optional[str] = Field()

    def __new__(cls, *args, **kwargs):
        event_cls = super().__new__(cls)
        event_cls.__fields__['event_name'].default_factory = cls.get_event_name
        return event_cls

    @classmethod
    def get_event_name(cls):
        raise NotImplementedError(f"get_event_name() is not implemented in {cls.__name__}")


class ExternalEvent(ABC, Event):
    """ The event type is unknown, so all the fields are in data. """
    data: Any

    def __init__(self, **kwargs):
        super(ExternalEvent, self).__init__(**kwargs)
        self.data = kwargs
        self.event_name = kwargs.get('event_name', None)


class AckEvent(ABC, Event):
    acknowledged: bool = False


__all__ = [
    'Event',
    'ExternalEvent',
    'AckEvent',
]
