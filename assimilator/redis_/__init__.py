from assimilator.core.services import CRUDService
from assimilator.redis_.database import RedisRepository, RedisUnitOfWork
from assimilator.core.usability.registry import register_pattern, PatternList

pattern_list = PatternList(
    repository=RedisRepository,
    uow=RedisUnitOfWork,
    crud=CRUDService,
)

register_pattern(provider='redis', pattern_list=pattern_list)
register_pattern(provider='redis_', pattern_list=pattern_list)
