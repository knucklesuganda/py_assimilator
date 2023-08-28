from examples.events.simple_events.dependencies import event_bus
from examples.events.simple_events.events import MusicRecordCreated, UserNotified


def create_record():
    event_bus.producer.produce(
        MusicRecordCreated(
            record_name="My song name",
            album="New music album",
            length=12,
        )
    )


@event_bus.consumer.register_callback(MusicRecordCreated)
def on_record_created(event: MusicRecordCreated, **_):
    print("New record:", event.record_name, "for album", event.album)
    event_bus.producer.produce(UserNotified(username="Andrey"))


@event_bus.consumer.register_callback(UserNotified)
def on_user_notified(event: UserNotified, **_):
    print("User with username", event.username, "was notified")


if __name__ == '__main__':
    event_bus.consumer.start(threaded=False)
    create_record()
