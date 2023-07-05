import inspect

from assimilator.core.events.events import Event
from assimilator.core.events.types import EventRegistrator


def get_event_name(event: EventRegistrator):
    if inspect.isclass(event):
        return event.event_name

    return event.event_name if isinstance(event, Event) else event


__all__ = [
    'get_event_name',
]
