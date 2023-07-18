from pydantic import Field

from assimilator.core.events.events import Event


class MusicRecordCreated(Event):
    record_name: str
    album: str
    length: int = Field(min=1)


class UserNotified(Event):
    username: str
