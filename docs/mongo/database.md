# Mongo Database patterns

Mongo patterns work with [MongoDB](https://www.mongodb.com/) NoSQL database.

## What patterns do we use?
Database, in our case, is a connection to MongoDB.

5 main patterns with databases:

- `MongoRepository` - works with the data. Saves, reads, updates, deletes, modifies, checks, filters our data.
- `MongoUnitOfWork` - works with MongoDB transactions. Ensures data integrity. Should only be used when the data is changed.
- `Specification` - some sort of filter for the repository. Filters, paginates, joins, limits the results in `MongoRepository`.
- `MongoSpecificationList` - contains links to `Specification` patterns for indirect coding.
- `LazyCommand` - database query that has been created, but not ran yet. Only runs the function when we need the results.

---------------------------------------------------------------------------------------

## Creating your models

The first thing that you have to do is create your Mongo models. PyAssimilator uses [Pydantic](https://docs.pydantic.dev/)
to develop models that are used as entities. We recommend using our `MongoModel` class to create your models:

```Python
# models.py
from assimilator.mongo.database.models import MongoModel

# Just a normal Pydantic model with cool things in it
class User(MongoModel):
    username: str
    email: str
    balance: float

    class AssimilatorConfig:
        collection = "users"    # collection in MongoDB

```

We recommend using `MongoModel` because it has various features such as:

- Automatic PyAssimilator configuration for better experience
- Parsing from/to JSON
- Automatic ObjectID generation
- Config for MongoDB collection

But, with that said, you could potentially use `BaseModel` from `Pydantic`. However, you are going to need
to create an ID field and add collection name:

```Python
# models.py
from bson import ObjectId
from pydantic import BaseModel

# Just a normal Pydantic model
class User(BaseModel):
    id: ObjectId     # id can be any type, but we use ObjectId from mongodb 
    username: str
    email: str
    balance: float

    class AssimilatorConfig:    # config for assimilator 
        collection = "users"    # add collection name

```


## Creating our patterns

Once you have your models, you are going to start creating your Mongo patterns. We are going to create
`MongoUnitOfWork` and `MongoRepository` to manage data and transactions:

```Python
# dependencies.py
from assimilator.mongo.database import MongoRepository, MongoUnitOfWork
from pymongo import MongoClient

from models import User

client = MongoClient()  # our mongodb connection


def get_repository():
    return MongoRepository(
        session=client,  # database session
        model=User,  # our main model
        database='assimilator_database',  # database name
    )


def get_uow():
    return MongoUnitOfWork(repository=get_repository())
```

`MongoRepository` must accept a `pymongo.MongoClient` for the session, the model that we created, and the name of the database
that we want to work with.

- `session` - [MongoClient](https://pymongo.readthedocs.io/en/stable/tutorial.html#making-a-connection-with-mongoclient) connection/
- `model` - Pydantic or MongoModel entity that you created.
- `database` - name of your database.

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
instead of their Mongo descendants.
We suggest you do the same in order to follow SOLID principles. 
"""


def create_user(uow: UnitOfWork):
    with uow:   # We use that to start the transaction
        repository = uow.repository   # access the repository from the MongoUnitOfWork

        # Save the user using Repository.save() function and by passing all the arguments inside
        new_user = repository.save(username="Andrey", balance=1000)

        # WARNING!!! We have not applied any changes up to that point.
        # We must call MongoUnitOfWork.commit() to change that: 
        uow.commit() 
        # Changes are applied and used is in the database!

    return new_user

created_user = create_user(get_uow())   # Create our MongoUnitOfWork


def get_user(repository: Repository):    # Only pass the Repository because we want to read the data
    return repository.get(  # Use get() to query one user from the database
        repository.specs.filter(    # Use filter specification to give your filtering criteria
            username="Andrey",
        )
    )

user = get_user(get_repository())
```

That's it. Nothing really changes from the basic tutorial, as all the things stay the same in all of our patterns.
However, there are specific things that you may not use, but still need to know. You can read about them below:


---------------------------------------------------------------------------------------

## Mongo Specifications

When we sort, filter, join and mutate our MongoDB data, we use Mongo specifications. Here is how they work, and what
you can do with them.

### `MongoFilter`
`MongoFilter` is used to filter your data using some filter. You can access it with one of the following
methods(ordered by code quality):

1. Indirect access from Repository:
```Python
# MongoFilter for repositories that use MongoSpecificationList
repository.specs.filter()
```

2. Direct access using an `import` statement:
```Python
from assimilator.mongo.database.specifications import MongoFilter, mongo_filter
# Both objects are the same

mongo_filter()
MongoFilter()
```

3. Direct access from an `MongoSpecificationList`:
```Python
from assimilator.mongo.database.specifications import MongoSpecificationList

MongoSpecificationList.filter()
```

If you want to add filters, then you can use filtering options or direct Mongo filters:

##### Filtering options:
```Python

repository.specs.filter(
    id=1,   # id == 1
    age__gt=18,     # age > 18
    username="Andrey",      # username == "Andrey"
    user_domain__like="%.com%",     # user_domain LIKE "%.com%"(yes, it works without SQL!)
)
```

You can check out our [Basic Tutorials](/tutorial/database/#data-querying) for more filtering options.


##### Direct filters:
Sometimes you don't want to use filtering options, or you have such a complicated query,
that filtering options do not allow you to fully execute it. Then, you can provide direct filters:

```Python
repository.specs.filter(
    # The same as username="Andrey" in filtering options
    # We use MongoDB query language here
    {'username': { "$eq": username }},
)
```

> You can find all the possible queries in [MongoDB documentation](https://www.mongodb.com/docs/manual/tutorial/query-documents/).

You can use that to create your own filters:
```Python

def only_adult_users():
    return {
        "age": {"$gt": 18},
    }


repository.specs.filter(
    only_adult_users(),
)

```

### `mongo_order` specification

`mongo_order` is a specification that you can use in order to sort your results.
You just provide the columns in your model that are going to be use for sorting.
For example:
```Python
# order by username
repository.specs.order('username')

# order by username and id
repository.specs.order('id', 'username')

# order by balance DESC with direct import
from assimilator.mongo.database.specifications import mongo_order
mongo_order('-balance')
```


### `mongo_paginate` specification

`mongo_paginate` is a specification that you can use to limit your results
You can provide `limit` and `offset` to paginate your data.

For example:
```Python
# only first 10
repository.specs.paginate(limit=10)

# all except for first 5
repository.specs.paginate(offset=5)

# offset by 10 and get the next 10 results
# with direct import
from assimilator.mongo.database.specifications import mongo_paginate
mongo_paginate(limit=10, offset=10)
```

### `mongo_join` specification
`mongo_join` is a specification that you can use to join multiple models together.
You only use it for back compatibility with other Repositories and to show that you are joining two entities together.
This specification only works as a dummy now. Here it's full code:
```Python

@specification
def Mongo_join(*targets: Collection, query: QueryT, **join_args: dict) -> QueryT:
    return query

```

> We don't think that it is necessary to join multiple entities together, and it's really memory inefficient. Instead, we 
> suggest that you use composition(store joined object in the model itself) to replicate foreign keys. We have some ideas
> on how to do real joins, but it is not implemented yet. 


For example:
```Python
# join by relationship name with addresses collection
repository.specs.join('addresses')

# join multiple entities
# with direct import
from assimilator.mongo.database.specifications import mongo_join
mongo_join('friends', 'he_he_he_ha')
```

### `mongo_only` specification
`mongo_only` is a specification that you can use to only select specific columns and optimize your queries.

Examples:
```Python

# Get only id and username columns
repository.specs.only('id', 'username')

# Get only balance column with direct import
from assimilator.mongo.database.specifications import mongo_only
mongo_only('balance')
```


### `MongoSpecificationList`
If you want to create your custom `SpecificationList` using `MongoSpecificationList` as a basis, then you can import it
like this:
```Python
from assimilator.mongo.database.specifications import MongoSpecificationList
```

---------------------------------------------------------------------------------------

## MongoModel

`MongoModel` is a special Pydantic model provided by PyAssimilator. It has a lot of interesting settings, and that part
will tell you about that.

### MongoModel configuration

`MongoModel` has a special inner-class called `AssimilatorConfig`. That class allows you to set up various values for your
model:

```Python
from typing import ClassVar

from assimilator.mongo.database import MongoModel


class User(MongoModel):
    username: str
    
    class AssimilatorConfig:
        collection: ClassVar[str]   # what is the name of the collection
        autogenerate_id: ClassVar[bool] = True  # should you autogenerate your ids

```

You can recreate that class and change the following values:

- `collection` - name of the collection for the model.
- `autogenerate_id` - whether to generate model's ID automatically. `True` by default.

If your `autogenerate_id` is `True`, then you can still provide a custom ID to the mode:
```Python
User(
    username="Andrey",
    id=ObjectId(),  # generate a new mongo ObjectId
)
```

But, if your `autogenerate_id` is `False`, then you **must** provide an ID to the constructor. 

### Special model values

- `upsert` - Whether to [upsert](https://www.mongodb.com/docs/drivers/node/current/fundamentals/crud/write-operations/upsert/) the model. `False` by default.
