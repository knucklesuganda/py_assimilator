from abc import abstractmethod
from typing import Iterator, Callable, List, Optional, final

from assimilator.core.events.events import Event
from assimilator.core.patterns.context_managers import StartCloseContextMixin


class EventConsumer(StartCloseContextMixin):
    def __init__(self, callbacks: Optional[List[Callable]] = None):
        if callbacks is None:
            callbacks = []

        self._callbacks: List[Callable] = callbacks

    @final
    def register(self, callback: Callable):
        self._callbacks.append(callback)

    @abstractmethod
    def consume(self) -> Iterator[Event]:
        raise NotImplementedError("consume() is not implemented")


class EventProducer(StartCloseContextMixin):
    @abstractmethod
    def produce(self, event: Event) -> None:
        raise NotImplementedError("produce() is not implemented")


class EventBus:
    def __init__(self, consumer: EventConsumer, producer: EventProducer):
        self.consumer = consumer
        self.producer = producer

    def produce(self, event: Event) -> None:
        self.producer.produce(event)

    def consume(self) -> Iterator[Event]:
        return self.consumer.consume()


__all__ = [
    'EventConsumer',
    'EventProducer',
    'EventBus',
]
