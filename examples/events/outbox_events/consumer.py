import redis

from assimilator.redis_.events.events_bus import RedisEventConsumer
from examples.events.outbox_events.events import OutboxEvent

consumer = RedisEventConsumer(session=redis.Redis(port=9000))


@consumer.register_callback(event=OutboxEvent)
def handle_event(event: OutboxEvent, **context):
    print(event)


consumer.start()
