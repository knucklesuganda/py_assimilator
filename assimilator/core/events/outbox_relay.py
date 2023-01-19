from abc import ABC
from typing import Iterable

from assimilator.core.database.unit_of_work import UnitOfWork
from assimilator.core.events.events import Event
from assimilator.core.events.events_bus import EventProducer


class OutboxRelay(ABC):
    def __init__(self, uow: UnitOfWork, producer: EventProducer):
        self.uow = uow
        self.producer = producer

    def start(self):
        raise NotImplementedError("start() is not implemented")

    def acknowledge(self, events: Iterable[Event]):
        raise NotImplementedError("acknowledge() is not implemented")


__all__ = [
    'OutboxRelay',
]
