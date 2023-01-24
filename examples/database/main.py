from core.database import UnitOfWork, Repository
from dependencies import get_alchemy_uow
from examples.database.models import AlchemyUser


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
        user = AlchemyUser(
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
    user = repository.get(repository.specs.filter(AlchemyUser.username == username))
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
                AlchemyUser(
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
        "Users with balance greater than 50:",
        repository.count(repository.specs.filter(balance__gt=50))
    )


if __name__ == '__main__':
    # create_user__kwargs(get_alchemy_uow())
    # create_user_model(get_alchemy_uow())

    # read_user(username="Andrey", repository=get_alchemy_uow().repository)
    # read_user_direct(username="Andrey-2", repository=get_alchemy_uow().repository)

    # update_user(get_alchemy_uow())
    # read_user(username="Andrey", repository=get_alchemy_uow().repository)

    # second_user = read_user(username="Andrey-2", repository=get_alchemy_uow().repository)
    # update_user_direct(user=second_user, uow=get_alchemy_uow())

    create_many_users(get_alchemy_uow())
    create_many_users_direct(get_alchemy_uow())

    uow = get_alchemy_uow()
    filter_users(uow.repository)
    count_users(uow.repository)
