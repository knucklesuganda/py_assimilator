from abc import ABC, abstractmethod

from assimilator.core.events.events import Event
from assimilator.core.patterns.context_managers import ContextManagedConnection


class EventConsumer(ContextManagedConnection):
    @abstractmethod
    def consume(self):
        raise NotImplementedError("consume() is not implemented")


class EventProducer(ContextManagedConnection):
    @abstractmethod
    def produce(self, event: Event):
        raise NotImplementedError("produce() is not implemented")


class EventBus(ABC):
    def __init__(self, consumer: EventConsumer, producer: EventProducer):
        self.consumer = consumer
        self.producer = producer

    @abstractmethod
    def produce(self, event: Event):
        self.producer.produce(event)

    @abstractmethod
    def consume(self):
        return self.consumer.consume()
