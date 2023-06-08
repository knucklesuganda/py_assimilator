from assimilator.core.services import CRUDService
from assimilator.core.usability.registry import register_pattern, PatternList
from assimilator.mongo.database import MongoRepository, MongoUnitOfWork

register_pattern(provider='mongo', pattern_list=PatternList(
    repository=MongoRepository,
    uow=MongoUnitOfWork,
    crud=CRUDService,
))
