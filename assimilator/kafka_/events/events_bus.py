from threading import Thread
from typing import Iterable, Optional, Type

import kafka
from kafka.errors import KafkaError

from assimilator.core.events.events import Event, ExternalEvent
from assimilator.core.events.utils import get_event_name
from assimilator.core.events.types import EventCallbackContainer
from assimilator.core.events.exceptions import EventProducingError
from assimilator.core.events.events_bus import EventConsumer, EventProducer


class KafkaEventConsumer(EventConsumer):
    def __init__(
        self,
        kafka_consumer: kafka.KafkaConsumer,
        callbacks: Optional[EventCallbackContainer] = None,
        events: Optional[Iterable[Type[Event]]] = None,
        manual_commit: bool = False,
    ):
        super(KafkaEventConsumer, self).__init__(callbacks=callbacks, events=events)
        self._kafka_client: kafka.KafkaConsumer = kafka_consumer
        self.manual_commit = manual_commit

    def run(self):
        self._kafka_client.subscribe([get_event_name(event) for event in self._events.keys()])

        for message in self._kafka_client:
            if not self.is_running:
                break

            self.consume(ExternalEvent.loads(message.value))

            if self.manual_commit:
                self._kafka_client.commit()


class KafkaEventProducer(EventProducer):
    def __init__(
        self,
        kafka_producer: kafka.KafkaProducer,
        sync_produce: bool = False,
        produce_timeout: Optional[int] = None,
    ):
        super(KafkaEventProducer, self).__init__()
        self._kafka_client = kafka_producer
        self.sync_produce = sync_produce
        self.produce_timeout = produce_timeout

    def produce(self, event: Event) -> None:
        message = self._kafka_client.send(topic=event.event_name, value=event.json().encode("utf-8"))

        if self.sync_produce:
            try:
                message.get(timeout=self.produce_timeout)
            except KafkaError as exc:
                raise EventProducingError(exc)

    def mass_produce(self, events: Iterable[Event]) -> None:
        for event in events:
            self.produce(event)


__all__ = [
    'KafkaEventConsumer',
    'KafkaEventProducer',
]
