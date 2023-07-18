from examples.events.outbox_events.events import OutboxEvent
from examples.events.outbox_events.producer.models import outbox


def main():
    outbox.produce(OutboxEvent(
        first_data=True,
        second_data="Hello!",
    ))


if __name__ == '__main__':
    main()
    outbox.start(threaded=True)
