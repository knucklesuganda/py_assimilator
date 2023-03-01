# Redis Database patterns

Redis patterns work with [Redis](https://redis.io/) in-memory database.
We use [PyRedis](https://redis.readthedocs.io/en/latest/) library to interact with it.

## What patterns do we use?
Database, in our case, is a dictionary object.

5 main patterns with databases:

- `RedisRepository` - works with the data. Saves, reads, updates, deletes, modifies, checks, filters our data.
- `RedisUnitOfWork` - works with Redis transactions. Ensures data integrity. Should only be used when the data is changed.
- `Specification` - some sort of filter for the repository. Filters, paginates, joins, limits the results in `RedisRepository`.
- `InternalSpecificationList` - contains links to `Specification` patterns for indirect coding.
- `LazyCommand` - database query that has been created, but not ran yet. Only runs the function when we need the results.


--------------------------------------------------------------------


## Creating your models

The first thing that you have to do is create your Redis models. PyAssimilator uses [Pydantic](https://docs.pydantic.dev/)
to develop models that are used as entities. We recommend using our `RedisModel` class to create your models:

```Python
# models.py
from assimilator.redis_.database.models import RedisModel

# Just a normal Pydantic model with cool things in it
class User(RedisModel):
    username: str
    email: str
    balance: float
```

We recommend using `RedisModel` because it has various features such as:

- Automatic PyAssimilator configuration for better experience
- Parsing from/to JSON
- Automatic ID generation
- Redis-related features

> RedisModel inherits BaseModel that we used in Internal patterns. 

But, with that said, you could potentially use `BaseModel` from `Pydantic`. However, you are going to need
to create an ID field and set `extra=True`:

```Python
# models.py
from pydantic import BaseModel

# Just a normal Pydantic model
class User(BaseModel, extra=True):  # extra values are allowed
    id: int     # id can be any type, but must be unique 
    username: str
    email: str
    balance: float
```

## Creating our patterns

Once you have your models, you are going to start creating your Redis patterns. We are going to create
`RedisUnitOfWork` and `RedisRepository` to manage data and transactions:


```Python
# dependencies.py
from redis import Redis
from assimilator.redis_.database import RedisRepository, RedisUnitOfWork

from models import User

database = Redis()      # connect to redis


def get_repository():
    return RedisRepository(
        session=database,  # database session is a dict
        model=User,     # our main model 
    )


def get_uow():
    return RedisUnitOfWork(repository=get_repository())
```

`RedisRepository` must accept `Redis` object from `pyredis` library and the model that we created.

- `session` - [Redis](https://redis.readthedocs.io/en/latest/connections.html) connection object.
- `model` - Pydantic or `RedisModel` entity that you created.

You can also see that instead of exporting our patterns as objects, we create a function that can be called to create
multiple objects whenever needed. The behaviour of creating one object or using object factories depends on your use
case, however, we suggest that you use different objects inside your code.


## Using our patterns

You already know how to use the patterns from our Basic Tutorial. So, here is that code again:
```Python

from assimilator.core.database import UnitOfWork, Repository
from dependencies import get_repository, get_uow

"""
We use base UnitOfWork and Repository annotations in our parameters 
instead of their redis descendants.
We suggest you do the same in order to follow SOLID principles. 
"""


def create_user(uow: UnitOfWork):
    with uow:   # We use that to start the transaction
        repository = uow.repository   # access the repository from the RedisUnitOfWork

        # Save the user using Repository.save() function and by passing all the arguments inside
        new_user = repository.save(username="Andrey", balance=1000)

        # WARNING!!! We have not applied any changes up to that point.
        # We must call RedisUnitOfWork.commit() to change that: 
        uow.commit() 
        # Changes are applied and used is in the database!

    return new_user

created_user = create_user(get_uow())   # create our RedisUnitOfWork


def get_user(repository: Repository):    # only pass the Repository because we want to read the data
    return repository.get(  # use get() to query one user from the database
        repository.specs.filter(    # use filter specification to give your filtering criteria
            username="Andrey",
        )
    )

user = get_user(get_repository())
```

--------------------------------------------------------------------

## Redis problems🥴

Redis is really fast, and we want to use that speed as our main advantage, however, it is really difficult to do now. 
We are going to change the way `RedisRepository` stores data once we find the best way to query it quickly. For now, we
just store the keys in the database and query most of them when we need to do something with our data. This may decrease
the performance, but it is a viable solution for lost of the projects.


--------------------------------------------------------------------

## Redis Specifications

Redis does not have its own specifications yet. We use [Internal Specifications](/internal/database/#internal-specifications)
for now.

The only thing that you should know is that it is always faster to query your data using the ID since we store our entities
as redis keys.


--------------------------------------------------------------------

## RedisModel

`RedisModel` is a special Pydantic model provided by PyAssimilator. It has a lot of interesting settings, and that part
will tell you about that.

### RedisModel configuration

`RedisModel` has a special inner-class called `AssimilatorConfig`. That class allows you to set up various values for your
model:

```Python
from typing import ClassVar

from assimilator.redis_.database import RedisModel


class User(RedisModel):
    username: str
    
    class AssimilatorConfig:
        autogenerate_id: ClassVar[bool] = True  # should you autogenerate your ids

```

You can recreate that class and change the following values:

- `autogenerate_id` - whether to generate model's ID automatically. `True` by default.

If your `autogenerate_id` is `True`, then you can still provide a custom ID to the model:
```Python
User(
    username="Andrey",
    id="custom-id",  # generate a new redis key
)
```

But, if your `autogenerate_id` is `False`, then you **must** provide an ID to the constructor. 

### Special model values

- `expire_in` - how many seconds should pass for that entity to be deleted. `None` by default.
- `expire_in_px` - how many milliseconds should pass for that entity to be deleted. `None` by default.
- `only_update` - only update this entity(no creation). `False` by default.
- `only_create` - only create this entity(no update). `False` by default.
- `keep_ttl` - whether to keep the TTL associated with this entity. `False` by default.
