from typing import Iterable

from redis import Redis

from assimilator.core.events import Event, ExternalEvent
from assimilator.core.events.events_bus import EventConsumer, EventProducer


class RedisEventConsumer(EventConsumer):
    def __init__(self, channels: Iterable[str], session: Redis):
        self.session = session
        self.channels = channels

    def close(self):
        self.session.close()

    def start(self):
        """ Connected by default """

    def consume(self) -> Iterable[ExternalEvent]:
        publish_subscribe = self.session.pubsub()
        publish_subscribe.subscribe(*self.channels)

        while True:
            message = publish_subscribe.get_message()

            if (message is None) or message['type'] != 'message':
                self.delay_function()
                continue

            yield ExternalEvent.loads(message['data'])
            self.delay_function()

    def delay_function(self):
        pass


class RedisEventProducer(EventProducer):
    def __init__(self, channel: str, session: Redis):
        self.session = session
        self.channel = channel

    def produce(self, event: Event):
        self.session.publish(self.channel, event.json())

    def start(self):
        pass

    def close(self):
        self.close()


__all__ = [
    'RedisEventConsumer',
    'RedisEventProducer',
]
