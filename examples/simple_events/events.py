from pydantic import Field

from assimilator.core.events.events import Event


class MusicRecordCreated(Event):
    @classmethod
    def get_event_name(cls):
        return "music_record_created"

    record_name: str
    album: str
    length: int = Field(min=1)


class UserNotified(Event):
    @classmethod
    def get_event_name(cls):
        return "user_notified"

    username: str
