from time import sleep
from abc import abstractmethod
from typing import Iterable, TypeVar, Dict, Union

from assimilator.core.events.events_bus import EventProducer
from assimilator.core.database.unit_of_work import UnitOfWork
from assimilator.core.events.events import Event, ExternalEvent
from assimilator.core.patterns.threaded_pattern import ThreadedPattern
from assimilator.core.database.specifications.adaptive import filter_

SavedEventT = TypeVar("SavedEventT")


class TransactionalOutbox(EventProducer, ThreadedPattern):
    def __init__(self, producer: EventProducer, events_uow: UnitOfWork, delay: float = 10):
        super(TransactionalOutbox, self).__init__()
        self.producer = producer
        self.delay = delay
        self.uow = events_uow

    @abstractmethod
    def get_event_data(self, event: SavedEventT) -> Union[dict, str]:
        raise NotImplementedError(f"get_event_data() is not implemented in {self.__class__.__name__}")

    @abstractmethod
    def create_event_model(self, event: Event) -> SavedEventT:
        raise NotImplementedError(f"save_event() is not implemented in {self.__class__.__name__}")

    def get_events(self) -> Iterable[Event]:
        raw_events: Iterable[SavedEventT] = self.uow.repository.filter()
        parsed_events = []

        for event in raw_events:
            event_data = self.get_event_data(event)

            if isinstance(event_data, Dict):
                parsed_events.append(ExternalEvent(**event_data))
            else:
                parsed_events.append(ExternalEvent.loads(event_data))

        return parsed_events

    def acknowledge_events(self, events: Iterable[Event]) -> None:
        for event in events:
            self.uow.repository.delete(filter_(id=event.id))

    def delay_outbox(self):
        sleep(self.delay)

    def run(self):
        while self.is_running:
            with self.uow:
                events = self.get_events()
                self.producer.mass_produce(events)
                self.acknowledge_events(events)
                self.uow.commit()

            self.delay_outbox()

    def produce(self, event: Event) -> None:
        with self.uow:
            self.uow.repository.save(self.create_event_model(event))
            self.uow.commit()

    def mass_produce(self, events: Iterable[Event]) -> None:
        with self.uow:
            for event in events:
                self.uow.repository.save(self.create_event_model(event))

            self.uow.commit()


__all__ = [
    'TransactionalOutbox',
]
