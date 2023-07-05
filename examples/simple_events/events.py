from pydantic import Field

from assimilator.core.events.events import Event


class MusicRecordCreated(Event):
    event_name: str = "music_record_created"

    record_name: str
    album: str
    length: int = Field(min=1)


class UserNotified(Event):
    event_name: str = "user_notified"
    username: str
