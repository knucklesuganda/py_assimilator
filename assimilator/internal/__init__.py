from assimilator.core.services import CRUDService
from assimilator.core.events.events_bus import EventBus
from assimilator.core.usability.registry import register_provider, PatternList
from assimilator.internal.database import InternalRepository, InternalUnitOfWork
from assimilator.internal.events import InternalEventConsumer, InternalEventProducer

register_provider(provider='internal', pattern_list=PatternList(
    repository=InternalRepository,
    uow=InternalUnitOfWork,
    crud=CRUDService,
    event_consumer=InternalEventConsumer,
    event_producer=InternalEventProducer,
    event_bus=EventBus,
))
