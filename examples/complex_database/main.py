from assimilator.core.patterns import LazyCommand
from assimilator.alchemy.database import AlchemyRepository
from assimilator.core.database import UnitOfWork, Repository
from assimilator.internal.database import InternalRepository, eq
from assimilator.redis_.database import RedisRepository

from dependencies import get_uow, User, Balance


def create_user__kwargs(uow: UnitOfWork):
    with uow:
        uow.repository.save(
            username='Andrey',
            email='python.on.papyrus@gmail.com',
            balances=[
                Balance(currency="USD", balance=2000),
                Balance(currency="HKD", balance=123456),
                Balance(currency="EUR", balance=50001),
            ]
        )
        uow.commit()


def create_user_model(uow: UnitOfWork):
    with uow:
        user = User(
            username='Andrey-2',
            email='python.on.papyrus@gmail.com',
        )

        user.balances.append(Balance(currency="USD", balance=0))
        uow.repository.save(user)
        uow.commit()


def read_user(username: str, balance: int, repository: Repository):
    user = repository.get(
        repository.specs.join('balances'),
        repository.specs.filter(
            username=username,
            balances__balance=balance,
            balances__currency="USD",
        ),
    )
    print("User:", user.id, user.username, user.email)

    for balance in user.balances:
        print(f"User {user.username} balance: ", balance.currency, balance.balance)

    return user


def read_user_direct(username: str, repository: Repository):
    if isinstance(repository, AlchemyRepository):       # Awful! Try to use filtering options
        user = repository.get(
            repository.specs.join('balances'),
            repository.specs.filter(User.username == username),
        )
    elif isinstance(repository, (InternalRepository, RedisRepository)):
        user = repository.get(
            repository.specs.filter(
                eq('username', username),
                # will call eq(model.username, username) for every user
            )
        )
    else:
        raise ValueError("Direct repository filter not found")

    print("User direct:", user.id, user.username, user.email)

    for balance in user.balances:
        print(f"User direct {user.username} balance: ", balance.currency, balance.balance)

    return user


def update_user(uow: UnitOfWork):
    with uow:
        user = uow.repository.get(
            uow.repository.specs.filter(
                username="Andrey",
            ),
        )

        user.balances[0].balance += 1000
        user.balances[1].balance = 0
        uow.repository.update(user)
        uow.commit()


def update_user_direct(user, uow: UnitOfWork):
    with uow:
        user.balances[0].balance /= 2
        uow.repository.update(user)
        uow.commit()


def create_many_users(uow: UnitOfWork):
    with uow:
        for i in range(100):
            uow.repository.save(
                username=f"User-{i}",
                email=f"user-{i}@py_assimilator.com",
                balances=[
                    Balance(currency="USD", balance=1000),
                ],
            )

        uow.commit()


def create_many_users_direct(uow: UnitOfWork):
    with uow:
        for i in range(100):
            uow.repository.save(
                User(
                    username=f"User-{i}",
                    email=f"user-{i}@py_assimilator.com",
                    balances=[
                        Balance(currency="EUR", balance=i * 10),
                    ]
                )
            )

        uow.commit()


def filter_users(repository: Repository):
    users = repository.filter(
        repository.specs.join('balances'),
        repository.specs.filter(balances__balance__gt=50),
    )

    for user in users:
        print("Filtered User:", user.id, user.username, user.email)


def count_users(repository: Repository):
    print("Total users:", repository.count())
    print(
        "Users with balances greater than 5000:",
        repository.count(
            repository.specs.join('balances'),
            repository.specs.filter(balances__balance__gt=5000, balances__currency="EUR")
        )
    )


def filter_users_lazy(repository: Repository):
    users: LazyCommand[User] = repository.filter(
        repository.specs.join('balances'),
        repository.specs.filter(balances__balance__eq=0),
        lazy=True,
    )

    for user in users:  # Queries the database here
        print("User without any money:", user.username, user.balances)


def update_many_users(uow: UnitOfWork):
    username_filter = uow.repository.specs.filter(username__like="User-%")

    with uow:
        for user in uow.repository.filter(username_filter):
            for balance in user.balances:
                balance.balance = 10

        uow.commit()

    for user in uow.repository.filter(username_filter, lazy=True):
        assert all(balance.balance == 10 for balance in user.balances)


def delete_many_users(uow: UnitOfWork):
    with uow:
        uow.repository.delete(uow.repository.specs.filter(
            username__regex=r'User-\w*',
        ))
        uow.commit()

    specs = uow.repository.specs
    assert uow.repository.count(specs.join('balances'), specs.filter(balances__balance=10)) == 0


if __name__ == '__main__':
    create_user__kwargs(get_uow())
    create_user_model(get_uow())

    read_user(username="Andrey", balance=2000, repository=get_uow().repository)
    read_user_direct(username="Andrey-2", repository=get_uow().repository)

    update_user(get_uow())
    read_user(username="Andrey", balance=3000, repository=get_uow().repository)

    second_user = read_user(username="Andrey-2", balance=0, repository=get_uow().repository)
    update_user_direct(user=second_user, uow=get_uow())

    create_many_users(get_uow())
    create_many_users_direct(get_uow())

    update_many_users(get_uow())
    delete_many_users(get_uow())

    persistent_uow = get_uow()
    filter_users(persistent_uow.repository)
    count_users(persistent_uow.repository)
    filter_users_lazy(persistent_uow.repository)
