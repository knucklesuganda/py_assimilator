

Right now you know how to interact with database using patterns from [Basic Tutorials](/tutorial/database/). But,
some information in these tutorials is not completely correct. One of the latest updates called Usability Update allowed
us to create patterns instantly without using functions described in tutorials.

> It is still important to know how to create patterns using your own functions, and some applications may prefer to use 
> that instead of new functions.

-----------------------------------------------

## Pattern registry

Pattern registry is a dictionary that contains all the providers and respective patterns. Provider is an external library,
data source or basically a set of patterns that you are using. Example of providers are: SQLAlchemy, Redis, MongoDB, Cassandra, etc.

Each provider corresponds to a `PatternList` which is basically a class that has our patterns.
In order to use the functions that create our patterns, we must register our provider first.

----------------------------------------------------

#### Registering the patterns

```python
from assimilator.core.usability.registry import register_provider, PatternList
from assimilator.internal.database import InternalRepository, InternalUnitOfWork
from assimilator.core.services import CRUDService

# Our pattern list:
internal_patterns = PatternList(
    repository=InternalRepository,
    uow=InternalUnitOfWork,
    crud=CRUDService,
)

# Register the patterns with provider's name:
register_provider(provider='internal', pattern_list=internal_patterns)
```

Fortunately, you don't have to do that most of the time. All providers inside PyAssimilator are already registered,
and other libraries which interact with PyAssimilator must register them as well. But, that is an option for you if you
want to change the registry.


The function that you will probably use a lot is `find_provider`:

```python
from assimilator.core.usability.registry import find_provider

# Finds and imports the module if it is not in the registry yet.
find_provider(provider_path='assimilator.alchemy')
```

> `find_provider()` is a function that just imports the module. If you are developing a library you still have to use
> `register_provider()`.

----------------------------------------------------

#### Interacting with the registry

You can find a provider using `get_pattern_list()`:

```python
from assimilator.core.usability.registry import get_pattern_list

alchemy_patterns = get_pattern_list('alchemy')
```

You can also unregister patterns using `unregister_provider()`:

```python
from assimilator.core.usability.registry import unregister_provider

unregister_provider('alchemy')
# Now, you will not be able to find SQLAlchemy patterns

```

You can also get a pattern class by its name using `get_pattern()`:

```python
from assimilator.core.usability.registry import get_pattern

alchemy_uow_cls = get_pattern(provider='alchemy', pattern_name='uow')
```

> However, this is a usability update, meaning that you won't have to use most of these functions. They are low-level,
> and are only useful when developing an extension library for PyAssimilator or for very specific tasks. 

## Creating the patterns

Let's finally create our patterns using Usability Update:

```python
from assimilator.core.usability.pattern_creator import create_uow, create_repository, create_crud

# Create repository:
repository = create_repository(provider='alchemy', model=User, session=alchemy_session())

# Create unit of work:
uow = create_uow(
    provider='mongo',
    model=Product,
    session=pymongo.client_session.ClientSession(),
    kwargs_repository={
        "database": "my_db"
    }
)

# Create crud service:
crud = create_crud(provider='internal', model=CustomModel, session={})
```

So, instead of writing three separate functions with all the configurations, we can just use a create_PATTERN NAME function
and easily add a new pattern to our code!

-------------------------------------------------
#### Custom creation arguments

Some patterns have custom arguments in init function, and you can also provide them like this:

```python
uow = create_uow(
    provider='mongo',
    model=Product,
    session=pymongo.client_session.ClientSession(),
    kwargs_repository={     # Custom kwargs for repository
        "database": "my_db",
    },
    kwargs_uow={
        "custom_argument": True,
    }
)
```
