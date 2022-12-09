import json
from datetime import datetime


class Event:
    id: int
    event_name: str
    event_date: datetime

    def __init__(self, **kwargs):
        self.event_date = datetime.now()

        for key, value in kwargs.items():
            setattr(self, key, value)

    def dict(self):
        return {
            "event_name": self.event_name,
            "event_date": self.event_date,
        }

    def json(self):
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, event_data: str):
        data = json.loads(event_data)
        return cls(**data)


class AckEvent(Event):
    acknowledged: bool = False
