import operator

from assimilator.alchemy.database import AlchemyRepository
from assimilator.core.patterns import LazyCommand
from assimilator.redis_.database import RedisRepository
from assimilator.core.database import UnitOfWork, Repository
from assimilator.internal.database import InternalRepository
from assimilator.internal.database.specifications.filtering_options import find_attribute

from dependencies import get_uow, User


def create_user__kwargs(uow: UnitOfWork):
    with uow:
        uow.repository.save(
            username='Andrey',
            email='python.on.papyrus@gmail.com',
            balance=1000,
        )
        uow.commit()


def create_user_model(uow: UnitOfWork):
    with uow:
        user = User(
            username='Andrey-2',
            email='python.on.papyrus@gmail.com',
            balance=2000,
        )
        uow.repository.save(user)
        uow.commit()


def read_user(username: str, repository: Repository):
    user = repository.get(repository.specs.filter(username=username))
    print("User:", user.id, user.username, user.email, user.balance)
    return user


def read_user_direct(username: str, repository: Repository):
    if isinstance(repository, AlchemyRepository):       # Awful! Try to use filtering options
        user = repository.get(repository.specs.filter(User.username == username))
    elif isinstance(repository, (InternalRepository, RedisRepository)):
        user = repository.get(repository.specs.filter(
            find_attribute(operator.eq, 'username', username),
            # will call eq(model.username, username) for every user
        ))
    else:
        raise ValueError("Direct repository filter not found")

    print("User direct:", user.id, user.username, user.email, user.balance)
    return user


def update_user(uow: UnitOfWork):
    with uow:
        user = uow.repository.get(
            uow.repository.specs.filter(
                username="Andrey",
            ),
        )

        user.balance += 1000
        uow.repository.update(user)
        uow.commit()


def update_user_direct(user, uow: UnitOfWork):
    with uow:
        user.balance += 1000
        uow.repository.update(user)
        uow.commit()


def create_many_users(uow: UnitOfWork):
    with uow:
        for i in range(100):
            uow.repository.save(
                username=f"User-{i}",
                email=f"user-{i}@py_assimilator.com",
                balance=i * 100,
            )

        uow.commit()


def create_many_users_direct(uow: UnitOfWork):
    with uow:
        for i in range(100):
            uow.repository.save(
                User(
                    username=f"User-{i}",
                    email=f"user-{i}@py_assimilator.com",
                    balance=i * 100,
                )
            )

        uow.commit()


def filter_users(repository: Repository):
    users = repository.filter(
        repository.specs.filter(balance__gt=50),
    )

    for user in users:
        print("Filtered User:", user.id, user.username, user.email, user.balance)


def count_users(repository: Repository):
    print("Total users:", repository.count())
    print(
        "Users with balance greater than 5000:",
        repository.count(repository.specs.filter(balance__gt=5000))
    )


def filter_users_lazy(repository: Repository):
    users: LazyCommand[User] = repository.filter(
        repository.specs.filter(balance__eq=0),
        lazy=True,
    )

    for user in users:  # Queries the database here
        print("User without any money:", user.username, user.balance)


def update_many_users(uow: UnitOfWork):
    username_filter = uow.repository.specs.filter(username__like="User-%")

    with uow:
        uow.repository.update(username_filter, balance=10)
        uow.commit()

    assert all(user.balance == 10 for user in uow.repository.filter(username_filter, lazy=True))


def delete_many_users(uow: UnitOfWork):
    with uow:
        uow.repository.delete(uow.repository.specs.filter(
            username__regex=r'User-\w*',
        ))
        uow.commit()

    assert uow.repository.count(uow.repository.specs.filter(balance=10)) == 0


if __name__ == '__main__':
    create_user__kwargs(get_uow())
    create_user_model(get_uow())

    read_user(username="Andrey", repository=get_uow().repository)
    read_user_direct(username="Andrey-2", repository=get_uow().repository)

    update_user(get_uow())
    read_user(username="Andrey", repository=get_uow().repository)

    second_user = read_user(username="Andrey-2", repository=get_uow().repository)
    update_user_direct(user=second_user, uow=get_uow())

    create_many_users(get_uow())
    create_many_users_direct(get_uow())

    update_many_users(get_uow())
    delete_many_users(get_uow())

    persistent_uow = get_uow()
    filter_users(persistent_uow.repository)
    count_users(persistent_uow.repository)
    filter_users_lazy(persistent_uow.repository)
