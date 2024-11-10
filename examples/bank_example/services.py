import random

from faker import Faker

from assimilator.core.database import UnitOfWork
from assimilator.core.services import CRUDService
from assimilator.core.usability.pattern_creator import create_uow
from examples.bank_example.dependencies import SessionCreator
from examples.bank_example.models import UserTransaction, User


fake = Faker()


def create_random_transactions():
    session = SessionCreator()
    users_uow = create_uow(provider='alchemy', model=User, session=session)
    transactions_uow = create_uow(provider='alchemy', model=UserTransaction, session=session)

    with users_uow:
        sender = users_uow.repository.save(username=fake.user_name(), email=fake.email())
        receiver = users_uow.repository.save(username=fake.user_name(), email=fake.email())

        for i in range(random.randint(0, 100)):
            transactions_uow.repository.save(
                balance_change=random.randint(0,),
                sender=None,
                receiver=None,
            )

        users_uow.commit()
