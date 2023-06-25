## The problem

We had a problem with pattern creation. You had to write three or more functions just to create a pattern, and we assume
that this was too much for an average user. So, that is why we changed the way you create your patterns in the
Usability update!

> You can read the full documentation on Pattern creation here: [How to create patterns](/tutorial/how_to_create/)

Here is an example on how we **used to** create CRUDService pattern:

```python

def get_repository():
    return MongoRepository(
        session=mongo_client,
        model=User,
        database='assimilator_complex'
    )


def get_uow():
    return MongoUnitOfWork(repository=get_repository())


def get_crud():
    return CRUDService(uow=get_uow())


crud = get_crud()

```


----------------------------------------------

## Our solution

Now, instead of writing three functions just to create a pattern, you can just call a function and pass all the parameters
inside it. For example, here is how we create a CRUDService:

```python

crud = create_crud(
    provider='alchemy',         # External library that we are using.
    model=User,                 # Model your CRUDService is going to work with.
    session=session_creator(),  # Database session.
)

```


## In-depth look

There are other functions that allow us to fully inject all the patterns into our new update. Firstly, we have
a pattern registry. Pattern registry is a dictionary that contains all the possible patterns with their provider names.
When we want to create a pattern, we use that pattern registry to find the class that we want to use.

You don't want to interact with pattern registry directly(it is a dictionary, and they do not have any structure in Python).
That is why we have the following functions:

- `register_provider()` - Allows you to register a new provider of your own. 
If you are developing a library that interacts with PyAssimilator, it is a good practice to register your provider.
This way, anyone can easily import your patterns with our new functions.
- `find_provider()` - Allows you to provide a module that should find and register your provider.
- `get_pattern_list()` - Returns a list of all patterns for a provider.
- `unregister_provider()` - Deletes a provider from the registry.
- `get_pattern()` - Low-level function that returns a pattern class.

To find out more about these functions, go to [How to create patterns](/tutorial/how_to_create/)
