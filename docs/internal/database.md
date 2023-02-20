# Internal Database patterns

Internal patterns work with Python data structures like dictionary, list, set, and others. You can use that if you don't
have a database yet, or just want to test how things will work in memory.

## What patterns do we use?
Database, in our case, is a dictionary object.

5 main patterns with databases:

- `InternalRepository` - works with the data. Saves, reads, updates, deletes, modifies, checks, filters our data.
- `InternalUnitOfWork` - works with internal transactions. Ensures data integrity. Should only be used when the data is changed.
- `Specification` - some sort of filter for the repository. Filters, paginates, joins, limits the results in `InternalRepository`.
- `InternalSpecificationList` - contains links to `Specification` patterns for indirect coding.
- `LazyCommand` - database query that has been created, but not ran yet. Only runs the function when we need the results.

-------------------

# STILL IN DEVELOPMENT

## Creating your models

The first thing that you have to do is create your internal models. You can use anything from SQLAlchemy module to create
your models. All mapping types, column types, tables, foreign keys, and other things are supported by PyAssimilator.

We are going to create `User` model using declarative mappings:

```Python
# models.py
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(url="sqlite:///:memory:")
Base = declarative_base()
DatabaseSession = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    username = Column(String())
    balance = Column(Float())


Base.metadata.create_all(engine)
```

It's the same model as we have in our Basic Tutorial.


## Creating our patterns

Once you have your models, you are going to start creating your Alchemy patterns. We are going to create
`AlchemyUnitOfWork` and `AlchemyRepository` to manage data and transactions:


```Python
# dependencies.py
from assimilator.alchemy.database import AlchemyUnitOfWork, AlchemyRepository

from models import DatabaseSession, User

def get_repository():
    return AlchemyRepository(
        session=DatabaseSession(),  # database session
        model=User,     # our main model 
    )


def get_uow():
    return AlchemyUnitOfWork(repository=get_repository())


```

`AlchemyRepository` must accept an SQLAlchemy session and a model that we created.

- `session` - [SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/session_basics.html) session to the database.
- `model` - the model that you created. 
You can read about different model mappings [here](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html).

You can also see that instead of exporting our patterns as objects, we create a function that can be called to create
multiple objects whenever needed. The behaviour of creating one object or using object factories depends on your use
case, HOWEVER, we suggest that you use different objects inside your code.


## Using our patterns

You already know how to use the patterns from our Basic Tutorial. So, here is that code again:
```Python

from assimilator.core.database import UnitOfWork, Repository
from dependencies import get_repository, get_uow

"""
We use base UnitOfWork and Repository annotations in our parameters 
instead of their SQLAlchemy descendants.
We suggest you do the same in order to follow SOLID principles. 
"""


def create_user(uow: UnitOfWork):
    with uow:   # We use that to start the transaction
        repository = uow.repository   # access the repository from the AlchemyUnitOfWork

        # Save the user using Repository.save() function and by passing all the arguments inside
        new_user = repository.save(username="Andrey", balance=1000)

        # WARNING!!! We have not applied any changes up to that point.
        # We must call AlchemyUnitOfWork.commit() to change that: 
        uow.commit() 
        # Changes are applied and used is in the database!

    return new_user

created_user = create_user(get_uow())   # create our AlchemyUnitOfWork


def get_user(repository: Repository):    # only pass the Repository because we want to read the data
    return repository.get(  # use get() to query one user from the database
        repository.specs.filter(    # use filter specification to give your filtering criteria
            username="Andrey",
        )
    )

user = get_user(get_repository())
```

That's it. Nothing really changes from the basic tutorial, as all the things stay the same in all of our patterns.
However, there are specific things that you may not use, but still need to know. You can read about them below:

## Alchemy Specifications

When we sort, filter, join and mutate our SQLAlchemy query, we use Alchemy specifications. Here is how they work, and what
you can do with them.

### `AlchemyFilterSpecification`
`AlchemyFilterSpecification` is used to filter your data using some filter. You can access it with one of the following
methods(ordered by code quality):

1. Indirect access from Repository:
```Python
# AlchemyFilterSpecification for repositories that use AlchemySpecificationList
repository.specs.filter()
```

2. Direct access using an `import` statement:
```Python
from assimilator.alchemy.database.specifications import alchemy_filter, AlchemyFilter
# Both objects are the same

alchemy_filter()
AlchemyFilter()
```

3. Direct access from an `AlchemySpecificationList`:
```Python
from assimilator.alchemy.database.specifications import AlchemySpecificationList

AlchemySpecificationList.filter()
```

If you want to add filters, then you can use filtering options or direct alchemy filters:

##### Filtering options:
```Python

repository.specs.filter(
    id=1,   # id == 1
    age__gt=18,     # age > 18
    username="Andrey",      # username == "Andrey"
    user_domain__like="%.com%",     # user_domain LIKE "%.com%"
)
```

You can check out our [Basic Tutorials](/tutorial/database/#data-querying) for more filtering options.


##### Direct filters:
Sometimes you don't want to use filtering options, or you have such a complicated query,
that filtering options do not allow you to fully execute it. Then, you can provide direct filters:

```Python
repository.specs.filter(
    # The same as in filtering options username="Andrey"
    User.username == "Andrey"
)
```

Direct filter is anything that can be added to an SQLAlchemy query to specify the results. 

But, we expose our SQLAlchemy dependency when using direct filters. If you want to also accounts for that, then you
can create your own specification that you can use later:

```Python
# specifications.py
from assimilator.core.database import specification


@specification
def filter_by_username(username: str, query):
    return query.where(User.username == username)


# services.py
# Then, you call your specification like this:
repository.filter(
    filter_by_username("Andrey")
)
```

This way, you can remove SQLAlchemy dependency from your code.


### `alchemy_order` specification

`alchemy_order` is a specification that you can use in order to sort your results.
You just provide the columns in your model that are going to be use for sorting.
For example:
```Python
# order by username
repository.specs.order('username')

# order by username and id
repository.specs.order('id', 'username')

# order by balance DESC with direct import
from assimilator.alchemy.database.specifications import alchemy_order
alchemy_order('-balance')
```


### `alchemy_paginate` specification

`alchemy_paginate` is a specification that you can use to limit your results
You can provide `limit` and `offset` to paginate your data.

For example:
```Python
# only first 10
repository.specs.paginate(limit=10)

# all except for first 5
repository.specs.paginate(offset=5)

# offset by 10 and get the next 10 results
# with direct import
from assimilator.alchemy.database.specifications import alchemy_paginate
alchemy_paginate(limit=10, offset=10)
```

### `alchemy_join` specification
`alchemy_join` is a specification that you can use to join multiple models together.
You can provide the name of the [relationship](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html#sqlalchemy.orm.relationship)
or the model itself. It's better to provide just the name, as it is indirect style.

For example:
```Python
# join by relationship name with addresses table
repository.specs.join('addresses')

# join by relationship itself with addresses table 
repository.specs.join(User.addresses)

# join by model
repository.specs.join(Address)

# join multiple entities
# with direct import
from assimilator.alchemy.database.specifications import alchemy_join
alchemy_join(User.addresses, 'friends', 'he_he_he_ha')
```

##### Join arguments:
Sometimes you need to provide additional arguments to your joins(You can read about them in SQLAlchemy docs).
You can do that as follows:

```Python
repository.specs.join(
    'addresses',
    join_args=[
        {
            'full': True    # full join for addresses
        },
    ],
)

# Here is an example with multiple joins
repository.specs.join(
    'addresses',
    User.friends,
    join_args=[
        {'full': True},     # full join for addresses
        {
            # custom join clause for User.friends
            "onclause": Friend.user_id == 1
        }
    ],
)
```

### `alchemy_only` specification
`alchemy_only` is a specification that you can use to only select specific columns and optimize your queries.

Examples:
```Python

# Get only id and username columns
repository.specs.only('id', 'username')

# Get only balance column with direct import
from assimilator.alchemy.database.specifications import alchemy_only
alchemy_only('balance')
```


### `AlchemySpecificationList`
If you want to create your custom `SpecificationList` using `AlchemySpecificationList` as a basis, then you can import it
like this:
```Python
from assimilator.alchemy.database.specifications import AlchemySpecificationList
```
