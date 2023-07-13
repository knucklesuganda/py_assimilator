from typing import Iterable, Optional, Set, Type

from redis import Redis
from redis.client import PubSub

from assimilator.core.events.utils import get_event_name
from assimilator.core.events.types import EventRegistrator
from assimilator.core.events.events import Event, ExternalEvent
from assimilator.core.events.events_bus import EventConsumer, EventProducer
from assimilator.core.events.types import EventCallbackContainer, EventCallback


class RedisEventConsumer(EventConsumer):
    def __init__(
        self,
        session: Redis,
        message_timeout: float = 1,
        callbacks: Optional[EventCallbackContainer] = None,
        events: Optional[Iterable[Type[Event]]] = None,
    ):
        super(RedisEventConsumer, self).__init__(callbacks=callbacks, events=events)
        self.session = session
        self._redis_channel: PubSub = session.pubsub()
        self._channels: Set[str] = set() if callbacks is None else set(callbacks.keys())
        self.message_timeout = message_timeout

    def register_callback(self, event: EventRegistrator, callback: EventCallback = None):
        event_name = get_event_name(event)

        if event_name not in self._channels:
            self._redis_channel.subscribe(event_name)
            self._channels.add(event_name)

        return super(RedisEventConsumer, self).register_callback(event=event, callback=callback)

    def run(self):
        while self.is_running:
            message = self._redis_channel.get_message(
                ignore_subscribe_messages=True,
                timeout=self.message_timeout,
            )

            if message is None:
                continue
            elif message.get('type') == 'message':
                self.consume(ExternalEvent.loads(message.get('data')))


class RedisEventProducer(EventProducer):
    def __init__(self, session: Redis):
        self.session = session

    def produce(self, event: Event, event_channel: str = None):
        event_name = get_event_name(event) if event_channel is None else event_channel
        self.session.publish(channel=event_name, message=event.json())

    def mass_produce(self, events: Iterable[Event], event_channel: str = None) -> None:
        for event in events:
            event_name = get_event_name(events) if event_channel is None else event_channel
            self.session.publish(channel=event_name, message=event.json())


__all__ = [
    'RedisEventConsumer',
    'RedisEventProducer',
]
