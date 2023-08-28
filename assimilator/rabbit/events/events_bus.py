from typing import Optional, Iterable, Type

import pika

from assimilator.core.events.events import Event
from assimilator.core.events.types import EventCallbackContainer
from assimilator.core.events.events_bus import EventConsumer, EventProducer


class RabbitEventConsumer(EventConsumer):
    def __init__(
        self,
        connection: pika.BlockingConnection,
        manual_commit: bool = True,
        callbacks: Optional[EventCallbackContainer] = None,
        events: Optional[Iterable[Type[Event]]] = None,
    ):
        super(RabbitEventConsumer, self).__init__(callbacks=callbacks, events=events)
        self.connection = connection.channel()
        self.manual_commit = manual_commit

    @staticmethod
    def _event_callback(channel, method, properties, body, queue_name):
        print(channel, method, properties, body, queue_name)

    def stop(self):
        self.connection.stop_consuming()
        super(RabbitEventConsumer, self).stop()

    def run(self):
        for event_name, event in self._events.items():
            self.connection.queue_declare(queue=event_name)
            self.connection.basic_consume(
                queue=event_name,
                on_message_callback=self._event_callback,
                auto_ack=self.manual_commit,
            )

        self.is_running = True
        self.connection.start_consuming()


class RabbitEventProducer(EventProducer):
    def __init__(self, connection: pika.BlockingConnection):
        super(RabbitEventProducer, self).__init__()
        self.connection = connection.channel()

    def produce(self, event: Event) -> None:
        event_name = event.get_event_name()

        self.connection.queue_declare(queue=event_name)
        self.connection.basic_publish(
            exchange='',
            routing_key=event_name,
            body=event.json().encode('utf-8'),
        )

    def mass_produce(self, events: Iterable[Event]) -> None:
        for event in events:
            self.produce(event)
