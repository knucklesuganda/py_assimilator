import json
from typing import Iterable

from kafka_ import KafkaConsumer, KafkaProducer
from kafka_.errors import KafkaError

from assimilator.core.events import Event, ExternalEvent
from assimilator.core.events import EventParsingError, EventProducingError
from assimilator.core.events.events_bus import EventConsumer, EventProducer


class KafkaEventConsumer(EventConsumer):
    def __init__(self, topics: Iterable[str], consumer: KafkaConsumer):
        self.consumer = consumer
        self.topics = list(topics)

    def close(self):
        self.consumer.close()

    def start(self):
        """ Connected by default """

    def consume(self) -> Iterable[ExternalEvent]:
        self.consumer.subscribe(self.topics)

        for message in self.consumer:
            try:
                yield ExternalEvent.parse(message.value)
            except json.JSONDecoder as exc:
                raise EventParsingError(exc)


class KafkaEventProducer(EventProducer):
    def __init__(self, topic: str, producer: KafkaProducer, sync_produce: bool = False, timeout: int = None):
        self.topic = topic
        self.producer = producer
        self.sync_produce = sync_produce
        self.timeout = timeout

    def produce(self, event: Event):
        message = self.producer.send(self.topic, key=event.id, value=event.json())

        if self.sync_produce:
            try:
                message.get(timeout=self.timeout)
            except KafkaError as exc:
                raise EventProducingError(exc)

    def start(self):
        """ Already started """

    def close(self):
        self.producer.close()


__all__ = [
    'KafkaEventConsumer',
    'KafkaEventProducer',
]
