from assimilator.core.events import EventProducer, EventConsumer
from examples.simple_events.dependencies import get_producer, get_consumer
from examples.simple_events.events import RecordCreated


def emit_event(producer: EventProducer):
    with producer:
        record_event = RecordCreated(record_name="firstRecord")
        producer.produce(record_event)


def consume_events(consumer: EventConsumer):
    with consumer:
        for event in consumer.consume():
            print(event)


if __name__ == '__main__':
    emit_event(get_producer())
    consume_events(get_consumer())
