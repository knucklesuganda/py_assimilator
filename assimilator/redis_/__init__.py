from assimilator.redis_.database import RedisRepository, RedisUnitOfWork
from assimilator.core.usability.registry import register_provider, PatternList
from assimilator.redis_.events.events_bus import RedisEventConsumer, RedisEventProducer

pattern_list = PatternList(
    repository=RedisRepository,
    uow=RedisUnitOfWork,
    event_consumer=RedisEventConsumer,
    event_producer=RedisEventProducer,
)

register_provider(provider='redis', pattern_list=pattern_list)
register_provider(provider='redis_', pattern_list=pattern_list)

__all__ = []
