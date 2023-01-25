# Assimilator - the best Python patterns for the best projects

![](/images/logo.png)

## Install now
* `pip install py_assimilator`


## Simple example

Example usage of the code to create a user using all the DDD patterns:
```Python
from assimilator.alchemy.database import AlchemyUnitOfWork, AlchemyRepository
from assimilator.core.database import UnitOfWork

from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(url="sqlite:///:memory:")
Base = declarative_base()
DatabaseSession = sessionmaker(bind=engine)


class User(Base):    # Create user model
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    username = Column(String())
    email = Column(String())
    balance = Column(Float())

    def __str__(self):
        return f"{self.id} {self.username} {self.email}"


Base.metadata.create_all(engine)


def create_user(username: str, email: str, uow: UnitOfWork):
    with uow:
        repository = uow.repository     # get Repository pattern from unit of work
        new_user = repository.save(username=username, email=email, balance=0)   # create the user
        uow.commit()    # Commit session with Unit of work pattern

    return new_user


user_repository = AlchemyRepository(session=DatabaseSession(), model=User)
user_uow = AlchemyUnitOfWork(repository=user_repository)

create_user(
    username="Andrey", 
    email="python.on.papyrus@gmail.com",
    uow=user_uow,
)

```
Hard? Don't worry, you will only have to memorize it once. After that, you just repeat the code!

## Source
* [Github](https://github.com/knucklesuganda/py_assimilator)
* [PyPI](https://pypi.org/project/py-assimilator/)
* [Documentation](https://knucklesuganda.github.io/py_assimilator/)
* [Github](https://github.com/knucklesuganda/py_assimilator)
* [Author's YouTube RU](https://www.youtube.com/channel/UCSNpJHMOU7FqjD4Ttux0uuw)
* [Author's YouTube ENG](https://www.youtube.com/channel/UCeC9LNDwRP9OfjyOFHaSikA)

## About patterns in coding
They are useful, but only to some extent. Most of them are not suitable for 
real life applications. DDD(Domain-driven design) is one of the most popular ways of development
today, but nobody explains how to write most of DDD patterns in Python. Even if they do, life gives you another
issue that cannot be solved with a simple algorithm. That is why [Andrey](https://www.youtube.com/channel/UCSNpJHMOU7FqjD4Ttux0uuw) created
a library for the patterns that he uses in his projects daily.

## Types of patterns
These are different use cases for the patterns implemented.

- Database - patterns for database/data layer interactions
- Events - projects with events or event-driven architecture

## Available providers
Providers are different patterns for external modules like SQLAlchemy or FastAPI.

- Alchemy(Database, Events) - patterns for [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) for both database and events.
- Kafka(Events) - patterns in [Kafka](https://kafka.apache.org/) related to events.
- Internal(Database, Events) - internal is the type of provider that saves everything in memory(dict, list and all the tools within your app).
- Redis(Database, Events) - redis_ allows us to work with [Redis](https://redis.io/) memory database.
- MongoDB(Database) - mongo allows us to work with [MongoDB](https://www.mongodb.com/) database.
