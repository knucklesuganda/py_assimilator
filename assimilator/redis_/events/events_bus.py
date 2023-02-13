from typing import Iterable, Optional

from redis import Redis
from redis.client import PubSub

from assimilator.core.events import Event, ExternalEvent
from assimilator.core.events.events_bus import EventConsumer, EventProducer


class RedisEventConsumer(EventConsumer):
    def __init__(self, channels: Iterable[str], session: Redis):
        self.session = session
        self.channels = channels
        self._event_channel: Optional[PubSub] = None

    def close(self):
        self._event_channel.close()
        self._event_channel = None

    def start(self):
        self._event_channel = self.session.pubsub()
        self._event_channel.subscribe(*self.channels)

    def consume(self) -> Iterable[ExternalEvent]:
        message = self._event_channel.get_message(ignore_subscribe_messages=True)

        while message is not None:
            if message['type'] == 'message':
                yield ExternalEvent.loads(message['data'])

            message = self._event_channel.get_message(ignore_subscribe_messages=True)


class RedisEventProducer(EventProducer):
    def __init__(self, channel: str, session: Redis):
        self.session = session
        self.channel = channel

    def produce(self, event: Event):
        self.session.publish(self.channel, event.json())

    def start(self):
        pass

    def close(self):
        pass


__all__ = [
    'RedisEventConsumer',
    'RedisEventProducer',
]
