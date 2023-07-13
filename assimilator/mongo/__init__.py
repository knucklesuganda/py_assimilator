from assimilator.core.usability.registry import register_provider, PatternList
from assimilator.mongo.database import MongoRepository, MongoUnitOfWork
from assimilator.mongo.events.event_bus import MongoEventConsumer, MongoEventProducer

register_provider(provider='mongo', pattern_list=PatternList(
    repository=MongoRepository,
    uow=MongoUnitOfWork,
    event_consumer=MongoEventConsumer,
    event_producer=MongoEventProducer,
))
