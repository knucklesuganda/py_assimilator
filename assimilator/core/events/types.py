from typing import Dict, Union, Type, Set, Protocol


class EventCallback(Protocol):
    def __call__(self, event: "Event", **context) -> None:
        ...


EventCallbackContainer = Dict[str, Set[EventCallback]]
EventRegistrator = Union[str, Type["Event"], "Event"]

__all__ = [
    'EventCallback',
    'EventCallbackContainer',
    'EventRegistrator',
]
