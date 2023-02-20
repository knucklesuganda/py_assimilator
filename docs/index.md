# Assimilator - the best Python patterns for the best projects

![](images/logo.png)

## Install now
* `pip install py_assimilator`


## Simple example

Example usage of the code to create a user using all the DDD patterns:
```Python
from assimilator.alchemy.database import AlchemyUnitOfWork, AlchemyRepository
from assimilator.core.database import UnitOfWork

def create_user(username: str, email: str, uow: UnitOfWork):
    with uow:
        repository = uow.repository     # Get Repository pattern
        new_user = repository.save(username=username, email=email, balance=0)
        uow.commit()    # Securely save the data

    return new_user


user_repository = AlchemyRepository(
    session=alchemy_session,    # alchemy db session
    model=User,     # alchemy user model 
)
user_uow = AlchemyUnitOfWork(repository=user_repository)

create_user(
    username="Andrey", 
    email="python.on.papyrus@gmail.com",
    uow=user_uow,
)

```

## Why do I need it?
![](images/why_assimilator_no_usage.png)

Patterns are very useful for good code, but only to some extent. Most of them are not suitable for 
real life applications. DDD(Domain-driven design) is one of the most popular ways of development
today, but nobody explains how to write most of DDD patterns in Python. Even if they do, life gives you another
issue that cannot be solved with a simple algorithm. That is why [Andrey](https://www.youtube.com/channel/UCSNpJHMOU7FqjD4Ttux0uuw) created
a library for the patterns that he uses in his projects daily.

![](images/why_assimilator_usage.png)

Watch our [Demo]() to find out more about pyAssimilator capabilities.

## Source
* [Github](https://github.com/knucklesuganda/py_assimilator)
* [PyPI](https://pypi.org/project/py-assimilator/)
* [Documentation](https://knucklesuganda.github.io/py_assimilator/)
* [Github](https://github.com/knucklesuganda/py_assimilator)
* [Author's YouTube RU](https://www.youtube.com/channel/UCSNpJHMOU7FqjD4Ttux0uuw)
* [Author's YouTube ENG](https://www.youtube.com/channel/UCeC9LNDwRP9OfjyOFHaSikA)


## Types of patterns
These are different use cases for the patterns implemented:

- Database - patterns for database/data layer interactions.
- Events(in development) - projects with events or event-driven architecture.
- Unidentified - patterns that are useful for different purposes.

## Available providers
Providers are different patterns for external modules like SQLAlchemy or FastAPI.

- Alchemy(Database, Events) - patterns for [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) for both database and events.
- Kafka(Events) - patterns in [Kafka](https://kafka.apache.org/) related to events.
- Internal(Database, Events) - internal is the type of provider that saves everything in memory(dict, list and all the tools within your app).
- Redis(Database, Events) - redis_ allows us to work with [Redis](https://redis.io/) memory database.
- MongoDB(Database) - mongo allows us to work with [MongoDB](https://www.mongodb.com/) database.
