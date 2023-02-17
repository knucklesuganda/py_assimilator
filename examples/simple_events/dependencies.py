import sys

import redis

from assimilator.internal.events import InternalEventProducer, InternalEventConsumer
from assimilator.redis_.events import RedisEventConsumer, RedisEventProducer

if len(sys.argv) == 1 or sys.argv[1] == "internal":
    event_storage = []

    def get_internal_consumer():
        return InternalEventConsumer(event_storage)

    def get_internal_producer():
        return InternalEventProducer(event_storage)

    get_producer = get_internal_producer
    get_consumer = get_internal_consumer

elif sys.argv[1] == "redis":
    redis_client = redis.Redis()

    def get_redis_consumer():
        return RedisEventConsumer(
            channels=["records"],
            session=redis_client,
        )

    def get_redis_producer():
        return RedisEventProducer(
            channel="records",
            session=redis_client,
        )

    get_producer = get_redis_producer
    get_consumer = get_redis_consumer

elif sys.argv[1] == "redis":
    User = RedisUser
    get_uow = get_redis_uow
    redis_session.flushdb()
