import random
from decimal import Decimal

from faker import Faker

from assimilator.core.usability.pattern_creator import create_repository, create_uow
from examples.bank_example.dependencies import SessionCreator
from examples.bank_example.models import User, UserTransaction
from examples.bank_example.specifications import transactions_statistics

fake = Faker()


def create_random_transactions():
    session = SessionCreator()
    users_uow = create_uow(provider="alchemy", model=User, session=session)
    transactions_uow = create_uow(
        provider="alchemy", model=UserTransaction, session=session
    )

    with users_uow:
        if random.random() > 0.5:
            sender = users_uow.repository.save(
                username=fake.user_name(), email=fake.email()
            )
        else:
            sender = users_uow.repository.filter()[0]

        if random.random() > 0.5:
            receiver = users_uow.repository.save(
                username=fake.user_name(), email=fake.email()
            )
        else:
            receiver = users_uow.repository.filter()[0]

        for i in range(random.randint(0, 100)):
            transactions_uow.repository.save(
                balance_change=random.randint(0, 1000),
                sender=sender,
                receiver=receiver,
            )

        users_uow.commit()


def get_transactions_statistics() -> dict[str, Decimal]:
    session = SessionCreator()
    transactions_repository = create_repository(
        provider="alchemy",
        model=UserTransaction,
        session=session,
    )

    return transactions_repository.get(transactions_statistics())
