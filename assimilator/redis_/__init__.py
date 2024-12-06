from assimilator.core.services import CRUDService
from assimilator.core.usability.registry import PatternList, register_provider
from assimilator.redis_.database import RedisRepository, RedisUnitOfWork

pattern_list = PatternList(
    repository=RedisRepository,
    uow=RedisUnitOfWork,
    crud=CRUDService,
)

register_provider(provider="redis", pattern_list=pattern_list)
register_provider(provider="redis_", pattern_list=pattern_list)
