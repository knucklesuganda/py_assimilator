from abc import abstractmethod
from time import sleep
from typing import Iterable, Union, Dict

from assimilator.core.events.events_bus import EventProducer
from assimilator.core.database.unit_of_work import UnitOfWork
from assimilator.core.events.events import Event, ExternalEvent
from assimilator.core.patterns.threaded_pattern import ThreadedPattern


class SavedEvent:
    @abstractmethod
    def get_event_data(self) -> Union[str, Dict]:
        raise NotImplementedError(f"get_event_data() is not implemented in {self.__class__.__name__}")


class TransactionalOutbox(ThreadedPattern):
    def __init__(self, producer: EventProducer, events_uow: UnitOfWork, delay: float = 10):
        super(TransactionalOutbox, self).__init__()
        self.producer = producer
        self.delay = delay
        self.uow: UnitOfWork = events_uow

    def get_events(self) -> Iterable[Event]:
        raw_events: Iterable[SavedEvent] = self.uow.repository.get()
        parsed_events = []

        for event in raw_events:
            event_data: str = event.get_event_data()
            parsed_events.append(ExternalEvent.loads(event_data))

        return parsed_events

    def acknowledge_events(self, events: Iterable[Event]) -> None:
        for event in events:
            self.uow.repository.delete(event)

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


__all__ = [
    'SavedEvent',
    'TransactionalOutbox',
]
