# from assimilator.internal.events.events_bus import InternalEventProducer, InternalEventConsumer
from assimilator.core.events.events_bus import EventBus
# consumer = InternalEventConsumer()
# producer = InternalEventProducer(consumer=consumer)
# event_bus = EventBus(consumer=consumer, producer=producer)

from redis.client import Redis
from redis_.events.events_bus import RedisEventConsumer, RedisEventProducer


redis = Redis()

consumer = RedisEventConsumer(session=redis)
producer = RedisEventProducer(session=redis)
event_bus = EventBus(consumer=consumer, producer=producer)

consumer.start(threaded=True)
