from assimilator.core.services import CRUDService
from assimilator.core.usability.registry import register_pattern, PatternList
from assimilator.internal.database import InternalRepository, InternalUnitOfWork

register_pattern(provider='internal', pattern_list=PatternList(
    repository=InternalRepository,
    uow=InternalUnitOfWork,
    crud=CRUDService,
))
