import sqlalchemy

from assimilator.core.services import CRUDService
from assimilator.core.usability.registry import register_provider, PatternList
from assimilator.alchemy.database import AlchemyRepository, AlchemyUnitOfWork


if sqlalchemy.__version__ < "2.0.0":
    raise RuntimeWarning(
        "PyAssimilator will only support SQLAlchemy 2 from now on. Please, update "
        "the library using this manual: https://docs.sqlalchemy.org/en/20/changelog/migration_20.html"
    )


register_provider(provider='alchemy', pattern_list=PatternList(
    repository=AlchemyRepository,
    uow=AlchemyUnitOfWork,
    crud=CRUDService
))
