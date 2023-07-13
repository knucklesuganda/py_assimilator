from typing import Optional, Iterable, Type

import pymongo

from assimilator.core.events.events import Event
from assimilator.core.events.events_bus import EventConsumer, EventProducer
from assimilator.core.events.types import EventCallbackContainer


class MongoEventConsumer(EventConsumer):
    def __init__(
        self,
        event_collection: pymongo.collection.Collection,
        callbacks: Optional[EventCallbackContainer] = None,
        events: Optional[Iterable[Type[Event]]] = None,
    ):
        super(MongoEventConsumer, self).__init__(callbacks=callbacks, events=events)
        self.collection = event_collection

    def run(self):
        with self.collection.watch([{
            "$match": {"operationType": "insert"}
        }]) as stream:
            for insert_change in stream:
                print(insert_change)


class MongoEventProducer(EventProducer):
    def __init__(self, event_collection: pymongo.collection.Collection):
        super(MongoEventProducer, self).__init__()
        self.event_collection = event_collection

    def produce(self, event: Event) -> None:
        self.event_collection.insert_one(event.dict())

    def mass_produce(self, events: Iterable[Event]) -> None:
        self.event_collection.insert_many(
            [event.dict() for event in events],
            ordered=True,
        )
