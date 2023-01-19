from assimilator.alchemy.database import AlchemyRepository, AlchemyUnitOfWork
from examples.alchemy.database.models import User, DatabaseSession


def create_repository():    # factory for RedisRepository
    return AlchemyRepository(session=DatabaseSession(), model=User)


def create_uow():  # factory for RedisUnitOfWork
    return AlchemyUnitOfWork(repository=create_repository())


__all__ = ['create_repository', 'create_uow']
