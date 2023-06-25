from assimilator.core.services import CRUDService
from assimilator.redis_.database import RedisRepository, RedisUnitOfWork
from assimilator.core.usability.registry import register_provider, PatternList

pattern_list = PatternList(
    repository=RedisRepository,
    uow=RedisUnitOfWork,
    crud=CRUDService,
)

register_provider(provider='redis', pattern_list=pattern_list)
register_provider(provider='redis_', pattern_list=pattern_list)
