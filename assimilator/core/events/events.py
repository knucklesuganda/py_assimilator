import re
from abc import ABC
from typing import Any, Optional

from pydantic import Field

from assimilator.core.database.models import BaseModel


class Event(BaseModel):
    event_name: Optional[str] = Field(default_factory=lambda: Event.get_event_name())

    def __new__(cls, *args, **kwargs):
        event_cls = super().__new__(cls)
        event_cls.__fields__['event_name'].default_factory = cls.get_event_name
        return event_cls

    @classmethod
    def get_event_name(cls):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()


class ExternalEvent(ABC, Event):
    """ The event type is unknown, so all the fields are in data. """
    data: Any

    def __init__(self, **kwargs):
        super(ExternalEvent, self).__init__(**kwargs)
        self.data = kwargs
        self.event_name = kwargs.get('event_name', None)

    @classmethod
    def get_event_name(cls):
        return cls.event_name

    def json(self, *args, **kwargs) -> str:
        data = super(ExternalEvent, self).dict(*args, **kwargs)
        return self.__class__.__config__.json_dumps(data.get('data'))


__all__ = [
    'Event',
    'ExternalEvent',
]
