from abc import ABC

from database.base.unit_of_work import UnitOfWork
from events.events_bus import EventBus


class OutboxRelay(ABC):
    def __init__(self, uow: UnitOfWork, event_bus: EventBus):
        self.uow = uow
        self.event_bus = event_bus

    def start(self):
        raise NotImplementedError("start() is not implemented")

    def acknowledge(self, events):
        raise NotImplementedError("acknowledge() is not implemented")
