import sys

import kafka
import pika
import pymongo
import redis

from assimilator.core.events.events_bus import EventBus
from assimilator.core.usability.registry import find_provider
from assimilator.core.usability.pattern_creator import create_event_consumer, create_event_producer
from assimilator.internal.events.events_bus import InternalEventConsumer, InternalEventProducer

provider = sys.argv[1] if len(sys.argv) > 1 else "internal"
find_provider(f"assimilator.{provider}")

if provider == "redis_":
    session = redis.Redis()
    kwargs_consumer = kwargs_producer = {"session": session}

elif provider == "kafka_":
    kwargs_consumer = {
        "kafka_consumer": kafka.KafkaConsumer(
            bootstrap_servers="localhost:9092",
            auto_offset_reset='earliest',
            group_id='consumer_group',
        ),
        "manual_commit": True,
    }
    kwargs_producer = {
        "kafka_producer": kafka.KafkaProducer(
            bootstrap_servers="localhost:9092"
        ),
    }

elif provider == "mongo":
    kwargs_producer = kwargs_consumer = {
        "event_collection": pymongo.MongoClient(
            host="localhost",
            port=30001,
            connectTimeoutMS=2000,
            socketTimeoutMS=2000,
        )['assimilator_events']['events'],
    }

elif provider == "rabbit":
    kwargs_producer = kwargs_consumer = {
        "connection": pika.BlockingConnection(parameters=pika.ConnectionParameters()),
    }

else:
    kwargs_consumer = {}
    kwargs_producer = {}


if provider != "internal":
    consumer = create_event_consumer(
        provider=provider, kwargs_consumer=kwargs_consumer,
    )
    producer = create_event_producer(
        provider=provider, kwargs_producer=kwargs_producer,
    )
else:
    consumer = InternalEventConsumer()
    producer = InternalEventProducer(consumer=consumer)

event_bus = EventBus(consumer=consumer, producer=producer)
