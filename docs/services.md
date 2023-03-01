Service is the main part of your business logic. It allows you to use all the patterns together, and you will probably
write services yourself. But, there are some classes that can help you with that.

----------------------------------------------------------

## CRUD Service Example

For example, you may want to write your own [CRUD](https://www.freecodecamp.org/news/crud-operations-explained/) services,
but, there is a class that helps you with this:

```Python
# dependencies.py
from assimilator.core.database import UnitOfWork
from assimilator.core.services.crud import CRUDService


def get_repository():   # create repository
    ...


def get_uow() -> UnitOfWork:  # create UnitOfWork
    ...


def get_service():
    """ This function creates CRUDService and accepts UnitOfWork as a parameter. """
    return CRUDService(uow=get_uow())

```

Then, we can integrate it with any web framework of our choice. I will use some pseudocode for that:

```Python
from web_framework import Router, Response
from assimilator.core.services import CRUDService

from dependencies import get_service

router = Router()


@router.list('/')
def list_all_users():
    service: CRUDService = get_service()
    # Use list function to get all users from the service
    return Response(service.list())
```

So, basically, `CRUDService` allows you to quickly create all the functions for data interactions using any kind of 
pattern.  You can also find a full [FastAPI example here](https://github.com/knucklesuganda/py_assimilator/tree/master/examples/fastapi_crud_example).


## CRUD Service methods

### `list`
This function allows you to return multiple entities. Used for Read operation in CRUD.

- `*filters` - any kind of filters passed to filter specification.
- `lazy` - whether to run `list()` as a lazy command. `False` by default.
- `**kwargs_filters` - any kind of filters passed to filter specification.

```Python
# For example, you may use it like this:

service.list(
    User.username.not_("Andrey"),   # Direct SQLAlchemy filter
    id__gt=20,  # only where id > 20
    lazy=True,  # as a lazy query
)
```

### `get`
This function allows you to return one entity. Used for Read operation in CRUD.

- `*filters` - any kind of filters passed to filter specification.
- `lazy` - whether to run `get()` as a lazy command. `False` by default.
- `**kwargs_filters` - any kind of filters passed to filter specification.

```Python
# For example, you may use it like this:

service.get(
    User.username == "Andrey",   # Direct SQLAlchemy filter
    id=20,  # only where id == 20
    lazy=True,  # as a lazy query
)
```

### `create`
This function allows you to create entities. Used for CREATE operation in CRUD.

- `obj_data` - `dict` with entity data or Model that you want to create.

```Python
# For example, you may use it like this:

service.create({
    "username": "Andrey",
    "balances": [   # Foreign key
        {
            "amount": 100,
            "currency": {   # Foreign key
                "name": "USD",
                "country": "USA",
            },
        },
    ],
})

# You may also provide the model itself:
user = User(username="Andrey")
user.balances.add(
    Balance(
        amount=100,
        currency=Currency(name="USD", country="USA")
    )
)

service.create(user)
```

The second method is direct, and we would advise you to you indirect methods(the first one with dict) when possible.


### `update`
This function allows you to update one entity. Used for Update operation in CRUD.

- `update_data` - dictionary of updated values
- `*filters` - any kind of filters passed to filter specification.
- `**kwargs_filters` - any kind of filters passed to filter specification.

```Python
# For example, you may use it like this:

service.update(
    id=1,   # user with ID 1
    update_data={
        "username": "Andrey-2",     # will have this new username
    },
)
```

> Important notice on foreign keys. We do not know how to effectively update them with indirect coding styles. So, update()
> only works with simple models now. But, you are free to override the function and put your foreign key handlers in there.
> Also, if you have an idea on how to improve update() or any other thing in Assimilator - be sure to open a pull request!


### `delete`
This function allows you to delete one entity. Used for Delete operation in CRUD.

- `*filters` - any kind of filters passed to filter specification.
- `**kwargs_filters` - any kind of filters passed to filter specification.

```Python
# For example, you may use it like this:

service.delete(
    id=1,   # delete user with id == 1
    username="Andrey",  # and username == "Andrey"
)
```

You can also find a full [FastAPI example here](https://github.com/knucklesuganda/py_assimilator/tree/master/examples/fastapi_crud_example).
