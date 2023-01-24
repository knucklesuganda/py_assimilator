from sqlalchemy.orm import sessionmaker

from alchemy.database import AlchemyUnitOfWork, AlchemyRepository
from examples.database.models import engine, AlchemyUser


def get_alchemy_uow():
    DatabaseSession = sessionmaker(bind=engine)
    repository = AlchemyRepository(
        session=DatabaseSession(),
        model=AlchemyUser,
    )

    return AlchemyUnitOfWork(repository)

