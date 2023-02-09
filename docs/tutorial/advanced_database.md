# Advanced database patterns usage

## Unit of work

When you are using `UnitOfWork` pattern you will typically call context managers(`with` statement) and `commit()` function. 
But, if you want to use all the functions of this pattern manually, you can do it like this:

```Python
from assimilator.core.database import UnitOfWork


def example(uow: UnitOfWork):
    uow.begin()     # begin the transaction
    
    try:
        uow.repository.save(username="Andrey", balance=1000)
        uow.commit()    # apply the changes
    except Exception as exc:
        uow.rollback()  # remove all the changes if there is an exception
    finally:
        uow.close()     # close the transaction
```

> However, most of the time, there is no need in doing that, and we recommend using `with uow:` instead.

---------------------------------------

## Writing your own specifications

Sometimes you are copying your specifications. That is bad, and can lead to many bugs and legacy code. Instead, you need
to identify the places where you copy your specifications, and your own specification that can be used easily.
Now, let's see how to do that.

### How do specifications work?
Specification is a class or a function that does the following: it gets your initial query, changes it, and returns the
new version. That is a simplified version of the source code for one of the internal specifications:
```Python
from typing import Optional

from assimilator.core.database import specification


@specification  # specification decorator
def internal_paginate(
    query: list,    # query from the repository
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> list:
    # we update the query with Python slices and return new variant
    return query[offset:limit]
```

Each specification must return an updated version of the query, or something that can be used logically with other specifications.
In this case, we get our query as a list of object, change the list, and return the updated version. 
So, each specification adds something to the query, and that updated query goes to the next specification.
After that, our `Repository` pattern applies the specifications and returns our new result!

> __**SUPER IMPORTANT**__. You are probably wondering: when do we get this query argument and how will the users pass 
> it to the specification? The `initial_query` argument that you provide in the `Repository` is your query, and you NEVER use
> query when you call specifications in your repository. The query is supplied automatically.

If you want to write your own specification, then you must choose between functional specifications and class-based
specifications. **We would suggest to use functional specifications whenever you can!**

---------------------------------------

### Functional specifications
Functional specifications are created with `@specification` decorator.
You must do the following to create a functional specification:

1. Create a function with `@specification` pattern.
2. Add any parameters and add query parameter as the last one.
3. Do something with the query in the function.
4. Return an updated query.

Let's say that we want to create a specification that only allows validated objects from a list:
```Python
from assimilator.core.database import specification

@specification
def validated_only(query: list):
    return list(filter(lambda obj: obj.validated, query))

```

Now, we can use that specification in our patterns:
```Python
from assimilator.core.database import Repository

from specifications import validated_only


def filter_all_validated(repository: Repository):
    return repository.filter(
        validated_only()    # always call the specification.
    )
```

If we want to add some arguments, we can easily do it. But, you must be sure that you are adding your arguments
before the `query` parameter:
```Python
from assimilator.core.database import specification

@specification
def validated_only(check_vip: bool, query: list):
    if check_vip:
        return list(filter(lambda obj: obj.validated and obj.is_vip, query))

    return list(filter(lambda obj: obj.validated, query))
```

We can use our updated specification like this:
```Python
from assimilator.core.database import Repository

from specifications import validated_only


def filter_all_validated(repository: Repository):
    return repository.filter(
        # We do not pass our query parameter. It is added automatically.
        validated_only(is_vip=True)
    )
```

---------------------------------------

### Class-based specifications

Class-based specifications are a little more advanced. You use them when you need auxiliary methods, inheritance, 
abstractions or anything else that classes can offer.

You can create them with these steps:

1. Create a class that inherits from `Specification`.
2. Add all the arguments that you need in the `__init__()` function.
3. Add `apply()` function from the `Specification` class.
4. Change the query and return it.

```Python
from assimilator.core.database import Specification


class ValidatedOnly(Specification):   # inherits from Specification abstract class
    def __init__(self, check_vip: bool):    # all the arguments go here
        super(ValidatedOnly, self).__init__()
        self.check_vip = check_vip

    # apply() will only get query as the argument.
    def apply(self, query: list) -> list:
        if self.check_vip:
            return list(filter(lambda obj: obj.validated and obj.is_vip, query))

        return list(filter(lambda obj: obj.validated, query))
```

We can use our class-based specification like this:
```Python
from assimilator.core.database import Repository

from specifications import ValidatedOnly


def filter_all_validated(repository: Repository):
    return repository.filter(
        ValidatedOnly(is_vip=True)        # Usage techniques are the same
    )
```

------------------------------

## Using SpecificationList pattern

What is the problem with our custom specifications? They are direct. We cannot use them if the query type changes,
so that means that we cannot use them with different repositories.

We can solve that issue with another pattern called `SpecificationList`. It allows you to map your specifications to
classes that can call different specifications for different repositories. When you use `repository.specifications` or
`repository.specs`, you are using `SpecificationList` objects from these repositories.

The most basic SpecificationList looks like this:

```Python
from typing import Type

from assimilator.core.database import FilterSpecification
from assimilator.core.database.specifications.types import (
    OrderSpecificationProtocol,
    PaginateSpecificationProtocol,
    OnlySpecificationProtocol,
    JoinSpecificationProtocol,
)


class SpecificationList:
    filter: Type[FilterSpecification]
    order: OrderSpecificationProtocol
    paginate: PaginateSpecificationProtocol
    join: JoinSpecificationProtocol
    only: OnlySpecificationProtocol
```

We have all the specifications that we talked about, and each specification has a [Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol)
typing that allows us to specify what arguments we need for specific pre-built specifications.

If you want to create your own `SpecificationList`, then be sure to do the following:

1. Create a class that inherits from `SpecificationList`.
2. Add all the pre-built specifications if your base class doesn't specify them.
3. Add your custom specifications.
4. Add your custom specification list to your repository.

```Python
from sqlalchemy.orm import Query

from assimilator.alchemy.database import AlchemySpecificationList
from assimilator.core.database import specification


@specification
def alchemy_validate(validate_vip: bool, query: Query):
    if validate_vip:
        return query.filter(is_vip=True, is_validated=True)

    return query.filter(is_validated=True)


class CustomSpecificationList(AlchemySpecificationList):
    # We don't need to specify pre-built specifications, 
    # we already have them in the AlchemySpecificationList
    validated = alchemy_validate
```

Then, we can use that specification list with any repository that works with alchemy:
```Python
from assimilator.alchemy.database import AlchemyRepository

from specifications import CustomSpecificationList


repository = AlchemyRepository(
    session=DatabaseSession(),
    model=User,
    specifications=CustomSpecificationList,     # Change specifications list
)


repository.filter(
    repository.specs.validated()    # use the specification indirectly
)
```

But, how do we make it so that the specification can work with other repositories? We have to write different specifications
and specification lists. There is just no other way(yet😎). So, if you want to use your specification with other patterns,
rewrite it to work with their data types and create a new SpecificationList that is going to be supplied in the Repository.
