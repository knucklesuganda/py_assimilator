from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from assimilator.alchemy import AlchemyRepository, AlchemyUnitOfWork
from assimilator.core.database import UnitOfWork
from assimilator.core.services import CRUDService
from examples.bank_example import settings
from examples.bank_example.models import Base
from examples.bank_example.models import Base as BaseModel
from examples.bank_example.models import User, UserTransaction

engine = create_engine(url=settings.DATABASE_URL)
SessionCreator = sessionmaker(bind=engine)


def create_tables():
    try:
        Base.metadata.create_all(engine)
        print("Created tables")
    except Exception:
        pass


def create_repository(model: BaseModel) -> AlchemyRepository:
    return AlchemyRepository(session=SessionCreator(), model=model)


def create_uow(model: BaseModel) -> UnitOfWork:
    return AlchemyUnitOfWork(repository=create_repository(model=model))


def create_user_service() -> CRUDService[User]:
    return CRUDService(uow=create_uow(model=User))


def create_transaction_service() -> CRUDService[User]:
    return CRUDService(uow=create_uow(model=UserTransaction))
