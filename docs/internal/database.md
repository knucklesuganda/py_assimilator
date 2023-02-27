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

## Creating your models

The first thing that you have to do is create your internal models. PyAssimilator uses [Pydantic](https://docs.pydantic.dev/)
to develop models that are used as entities. We recommend using our `BaseModel` class to create your models:

```Python
# models.py
from assimilator.core.database.models import BaseModel

# Just a normal Pydantic model with cool things in it
class User(BaseModel):
    username: str
    email: str
    balance: float
```

We recommend using `BaseModel` because it has various features such as:

- Automatic PyAssimilator configuration for better experience
- Parsing from/to JSON
- Automatic ID generation

But, with that said, you could potentially use `BaseModel` from `Pydantic`. However, you are going to need
to create an ID field:

```Python
# models.py
from pydantic import BaseModel

# Just a normal Pydantic model
class User(BaseModel):
    id: int     # id can be any type, but must be unique 
    username: str
    email: str
    balance: float
```


## Creating our patterns

Once you have your models, you are going to start creating your Internal patterns. We are going to create
`InternalUnitOfWork` and `InternalRepository` to manage data and transactions:


```Python
# dependencies.py
from assimilator.internal.database import InternalRepository, InternalUnitOfWork

from models import User

database = {}   # our data storage


def get_repository():
    return InternalRepository(
        session=database,  # database session is a dict
        model=User,     # our main model 
    )


def get_uow():
    return InternalUnitOfWork(repository=get_repository())
```

`InternalRepository` must accept a `dict()` for the session and the model that we created.

- `session` - Python dictionary or it's descendants.
- `model` - Pydantic or BaseModel entity that you created.

You can also see that instead of exporting our patterns as objects, we create a function that can be called to create
multiple objects whenever needed. The behaviour of creating one object or using object factories depends on your use
case, however, we suggest that you use different objects inside your code.


## Extending the session

Sometimes we want to use multiple repositories with different entities in them. If that is the case, then
we can use our sessions like this:

```Python

session = {
    "users": {},     # for User entity
    "products": {},     # for Product entity
}

def get_repository():
    return InternalRepository(
        session=database['users'],  # using nested dict as a session
        model=User,     # our main model 
    )

```


## Using our patterns

You already know how to use the patterns from our Basic Tutorial. So, here is that code again:
```Python

from assimilator.core.database import UnitOfWork, Repository
from dependencies import get_repository, get_uow

"""
We use base UnitOfWork and Repository annotations in our parameters 
instead of their Internal descendants.
We suggest you do the same in order to follow SOLID principles. 
"""


def create_user(uow: UnitOfWork):
    with uow:   # We use that to start the transaction
        repository = uow.repository   # access the repository from the InternalUnitOfWork

        # Save the user using Repository.save() function and by passing all the arguments inside
        new_user = repository.save(username="Andrey", balance=1000)

        # WARNING!!! We have not applied any changes up to that point.
        # We must call InternalUnitOfWork.commit() to change that: 
        uow.commit() 
        # Changes are applied and used is in the database!

    return new_user

created_user = create_user(get_uow())   # create our InternalUnitOfWork


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

## Internal Specifications

When we sort, filter, join and mutate our Internal data, we use Internal specifications. Here is how they work, and what
you can do with them.

### `InternalFilter`
`InternalFilter` is used to filter your data using some filter. You can access it with one of the following
methods(ordered by code quality):

1. Indirect access from Repository:
```Python
# InternalFilter for repositories that use InternalSpecificationList
repository.specs.filter()
```

2. Direct access using an `import` statement:
```Python
from assimilator.internal.database.specifications import InternalFilter, internal_filter
# Both objects are the same

internal_filter()
InternalFilter()
```

3. Direct access from an `InternalSpecificationList`:
```Python
from assimilator.internal.database.specifications import InternalSpecificationList

InternalSpecificationList.filter()
```

If you want to add filters, then you can use filtering options or direct internal filters:

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
from assimilator.internal.database.specifications import eq

repository.specs.filter(
    # The same as username="Andrey" in filtering options
    eq('username', "Andrey")
)
```

Internal direct filters are special functions that can change the query and specify what we want to get.
There is a module with all of them that you can import like this:
```Python
from assimilator.internal.database.specifications import internal_operator

internal_operator.eq('username', "Andrey")
internal_operator.gt('age', 18)
```

They are written to replicate Python's [operator](https://docs.python.org/3/library/operator.html) library. However, there
is another function called `find_attribute()`, and it is used to find any attribute and call a boolean function on it.
Here is how it works:
```Python
from assimilator.internal.database.specifications import find_attribute

# The following function is the same as internal_operator.eq('username', "Andrey")
find_attribute(
    func=lambda a, b: a == b,   # boolean function that compares field to value
    field='username',   # field that we want to get from an object
    value="Andrey",     # value that we want to compare our object's field to
)
```

You can use that function to create your own filters. Be sure to pass a real field with a boolean function:
```Python
from assimilator.internal.database.specifications import find_attribute


def only_adult_users():
    return find_attribute(
        func=lambda age_field, val: age_field == val,
        field='age',
        value=18,
    )


repository.specs.filter(
    only_adult_users(),
)

```

But, you can also create specifications. However, when work with internal specifications, we need to
make them a little differently. The thing is, that default Python structures do not support: regex, complex filters, joins,
pagination and so on. So, what we can do is just run the specifications on results instead of the query itself. But, that
would highly impact our algorithms, because sometimes we just need to get a value by its key. So, what do we do?

We break one important programming principle💀 called Single Responsibility Principle. 
Instead of just working with the query, we also write a specification for the list of models. Here is an example: 

```Python
# specifications.py
from assimilator.core.database import specification


@specification
def filter_by_username(username: str, query):
    if username == "Andrey" and isinstance(query, str):
        return "1"

    for model in query:
        if model.username == username:
            return model

    return None

# services.py
# Then, you call your specification like this:
repository.filter(
    filter_by_username("Andrey")
)
```

Here is what we did:

1. Internal Repository runs your specifications twice - with query as a string(dict key), and with query as a list of models.
2. We check that if query is a string(the first run), and our username is "Andrey", then we can return a dictionary key(id) which represents that user in the database
3. Otherwise, we go through each model and check that it's username is "Andrey".

Here is what we achieve with that code:

1. If we want to find Andrey in the database - we just return a string key for a dictionary: O(1)
1. If we can't use a simple algorithm - we go through each user: O(N)

It's still a debate if we will leave that or not, but that can optimize our code a lot. Imagine that we have a big
database with millions of users, and we want to find our entity by its ID. If that is the case, that would be very beneficial,
but maybe there is another way of doing so.

IMPORTANT: You don't always need to do something with string query in your specifications. If you are sure that the operation
cannot be used in a normal dictionary indexing, then you can do the following:
```Python
# specifications.py
@specification
def filter_by_username(username: str, query):
    # This specification only works with list query
    if isinstance(query, str):
        return query    # Do not modify the query

    for model in query:
        if model.username == username:
            return model

    return None
```


### `internal_order` specification

`internal_order` is a specification that you can use in order to sort your results.
You just provide the columns in your model that are going to be use for sorting.
For example:
```Python
# order by username
repository.specs.order('username')

# order by username and id
repository.specs.order('id', 'username')

# order by balance DESC with direct import
from assimilator.internal.database.specifications import internal_order
internal_order('-balance')
```


### `internal_paginate` specification

`internal_paginate` is a specification that you can use to limit your results
You can provide `limit` and `offset` to paginate your data.

For example:
```Python
# only first 10
repository.specs.paginate(limit=10)

# all except for first 5
repository.specs.paginate(offset=5)

# offset by 10 and get the next 10 results
# with direct import
from assimilator.internal.database.specifications import internal_paginate
internal_paginate(limit=10, offset=10)
```

### `internal_join` specification
`internal_join` is a specification that you can use to join multiple models together.
You only use it for back compatibility with other Repositories and to show that you are joining two entities together.
This specification only works as a dummy now. Here it's full code:
```Python

@specification
def internal_join(*targets: Collection, query: QueryT, **join_args: dict) -> QueryT:
    return query

```

> We don't think that it is necessary to join multiple entities together, and it's really memory inefficient. Instead, we 
> suggest that you use composition(store joined object in the model itself) to replicate foreign keys. We have some ideas
> on how to do real joins, but it is not yet implemented. 


For example:
```Python
# join by relationship name with addresses table
repository.specs.join('addresses')

# join multiple entities
# with direct import
from assimilator.internal.database.specifications import internal_join
internal_join('friends', 'he_he_he_ha')
```

### `internal_only` specification
`internal_only` is a specification that you can use to only select specific columns and optimize your queries.

Examples:
```Python

# Get only id and username columns
repository.specs.only('id', 'username')

# Get only balance column with direct import
from assimilator.internal.database.specifications import internal_only
internal_only('balance')
```


### `InternalSpecificationList`
If you want to create your custom `SpecificationList` using `InternalSpecificationList` as a basis, then you can import it
like this:
```Python
from assimilator.internal.database.specifications import InternalSpecificationList
```
