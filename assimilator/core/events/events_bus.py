from abc import abstractmethod
from typing import Callable, Optional, final, List, Iterable, Union, Dict, Any

from assimilator.core.events.events import Event
from assimilator.core.events.types import EventCallbackContainer, EventCallback, EventRegistrator
from assimilator.core.events.utils import get_event_name


class EventConsumer:
    def __init__(self, callbacks: Optional[EventCallbackContainer] = None):
        super(EventConsumer, self).__init__()
        self._callbacks: EventCallbackContainer = callbacks or {}

    def decorate_callback(self, event: EventRegistrator):

        def _callback_decorator(func: EventCallback):
            self.register_callback(event=event, callback=func)
            return func

        return _callback_decorator

    def register_callback(self, event: EventRegistrator, callback: EventCallback = None) -> Union[None, Callable]:
        if callback is None:    # TODO: should I do this because no overload in Python?
            return self.decorate_callback(event)

        event_name = get_event_name(event)

        if self._callbacks.get(event_name) is not None:
            self._callbacks[event_name].add(callback)
        else:
            self._callbacks[event_name] = {callback}

    def unregister_callback(self, event: EventRegistrator, callback: EventCallback):
        self._callbacks[event].remove(callback)

    def _get_context(self) -> Dict[str, Any]:
        return {
            "consumer": self,
        }

    def consume(self, event: Event):
        context = self._get_context()

        for callback in self.get_callbacks(event):
            callback(event, **context)

    def get_callbacks(self, event: EventRegistrator) -> List[EventCallback]:
        return self._callbacks.get(get_event_name(event), [])


class EventProducer:
    @abstractmethod
    def produce(self, event: Event) -> None:
        raise NotImplementedError("produce() is not implemented")

    @abstractmethod
    def mass_produce(self, events: Iterable[Event]) -> None:
        raise NotImplementedError("mass_produce() is not implemented")


class EventBus:
    def __init__(self, consumer: EventConsumer, producer: EventProducer):
        self._consumer = consumer
        self._producer = producer

    @property
    def producer(self):
        return self._producer

    @property
    def consumer(self):
        return self._consumer


__all__ = [
    'EventConsumer',
    'EventProducer',
    'EventBus',
    'EventCallback',
    'EventCallbackContainer',
]
