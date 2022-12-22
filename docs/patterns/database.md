# Database patterns

## Repository
Repository is the pattern that makes a virtual collection out of the database.
When we use a database we often have some kind of library, language or protocol.
If we want to make the database abstract, we use the repository pattern. It has basic
functions that help us change and query our data from any source. The beauty of the pattern
is that you can use it with SQL, text files, cache, S3, external API's or any kind of data storage.


###### `__init__()`
- `session` - each repository has a session that works as the primary data source. It can be your database connection, a text file or a data structure.
- `initial_query` - the initial query that you use in the data storage. We will show how it works later. It can be an SQL query, a key in the dictionary or anything else.
- `specifications: SpecificationList` - an object that contains links to the specifications that are used to create your queries

###### `_get_initial_query()`
returns the initial query used in the `_apply_specifications()`

###### `_apply_specifications()`
Applies Specifications to the query. **Must not be used directly.** apply
specifications gets a list of specifications and applies them to the query returned
in _get_initial_query(). The idea is the following: each specification gets a query and
adds some filters to it. At the end we get a fully working query modified with the
specifications provided by the user.
- `specifications: Iterable[Specifications]` - an iterable of specifications that can be used to specify some conditions in the query
> Specification is a pattern that adds filters or anything
else that specifies what kind of data we want.


###### `get()`
get is the function used to query the data storage and return one entity. You supply a list
of specifications that get you the entity from the storage.
- `specifications: Specifications` - specifications that can be used to specify some conditions in the query
- `lazy: bool` - whether you want to execute your query straight away or just build it  for the future
- `initial_query = None` - if you want to change the initial query for this query only, then you can provide it as an argument

###### `filter()`
filters is the function used to query the data storage and return many entities. You supply a list
of specifications that filter entities in the storage.
- `specifications: Specifications` - specifications that can be used to specify some conditions in the query
- `lazy: bool` - whether you want to execute your query straight away or just build it  for the future
- `initial_query = None` - if you want to change the initial query for this query only, then you can provide it as an argument

###### `save()`
Adds the objects to the session, so you can commit it latter. This method
should not change the final state of the storage, we have UnitOfWork for this(*do not commit your changes, just add them*).

###### `delete()`
Deletes the objects from the session, so you can commit it latter. This method
should not change the final state of the storage, we have UnitOfWork for this(*do not commit your changes, just delete them from your session*).

###### `update()`
Updates the objects in the session, so you can commit it latter. This method
should not change the final state of the storage, we have UnitOfWork for this(*do not commit your changes, just update them in your session*).

###### `is_modified()`
Checks whether an obj was modified or not. If any value changes within the object,
then it must return True

###### `refresh()`
Updates the object values with the values in the data storage. That can be useful if
you want to create an object and get its id that was generated in the storage, or if you
just want to have the latest saved version of the object.

###### `count()`
Counts the objects while applying specifications to the query. Give no specifications to 
count the whole data storage.
- `specifications: Specifications` - specifications that can be used to specify some conditions in the query
- `lazy: bool` - whether you want to execute your query straight away or just build it  for the future


### Creating your own repository:
If you want to create your own repository, then you are going to have to override all the functions above.
But, please, do not make new functions available to the outer world.

You can do this:
```python
from assimilator.core.database import BaseRepository

class UserRepository(BaseRepository):
    def _users_private_func(self):
        # Cannot be called outside
        return 'Do something'

```
And call that function inside of your repository. But, never do this:
```python
from assimilator.core.database import BaseRepository

class UserRepository(BaseRepository):
    def get_ser_by_id(self):
        # Cannot be called outside
        return self.get(filter_specification(id=1))

```
Since it is going to be really hard for you to replace one repository to another. Example:


```python
from assimilator.core.database import BaseRepository
from users.repository import UserRepository
from products.repository import ProductRepository


def get_by_id(id, repository: BaseRepository):
    return repository.get(filter_specification(id=1))


get_by_id(UserRepository())
get_by_id(ProductRepository()) 
# You can call the function with both repositories, and it will probably work fine
```


### How to create  my repositories?
You want to create a repository for entities in your projects. That means, that if you
have some auxiliary table in your app, then it probably should not have a repository. But, things
like Users, Products, Orders and others might have their own repository. That does not mean
that you will create a lot of classes, *but please do not add repositories for every class
in your system*. If you want to read more, please, look into the Domain-Driven Development books. 


## Specification
Specification is the pattern that adds values, filters, joins or anything else
to the query in your repository. It can also work as a filter for your objects.

#### Class-based specifications
```python
class Specification(ABC):
    @abstractmethod
    def apply(self, query):
        raise NotImplementedError("Specification must specify apply()")

    def __call__(self, query):
        return self.apply(query)
```

`apply(query) -> query`
apply is the main functions that you are going to override. It is used
in order to specify new things in your query. You get the query in the
specification and return an updated version of query.

For example, if your query has a filter function, and you want to filter by username, then you can create this:
```python
from assimilator.core.database import Specification

class UsernameSpecification(Specification):
    def __init__(self, username: str):
        super(UsernameSpecification, self).__init__()
        self.username = username

    def apply(self, query):
        return query.filter(username=username)
```

Here we do the following:
1) save the username in the constructor
2) override apply() and return an updated version of the query provided

The usage of this specification will look like this:

```python
repository = UserRepository(session)
user = repository.get(UsernameSpecification(username="python.on.papyrus"))
```
The repository will apply the specification and return the results.

#### Functional specifications
`__call__()` functions receives the query and call `apply()` in the specification.
This is used in order to make functional specifications possible.
`__call__()` allows you to call an object as a function: `obj()`.
This way, we can use functional specifications and class-based specifications
together.

If you want to create a functional specification, then you need to use the `@specification`
decorator:

```python
from assimilator.core.database import specification

@specification
def username_filter(query, username: str):
    return query.filter(username=username)
```

The function above is the equivalent of the `UsernameSpecification` class. Then,
you are going to use it like this:

```python
repository = UserRepository(session)
user = repository.get(username_filter(username="python.on.papyrus"))
```

Both types work the same, so you can choose the type of specifications that you like.
But, you can also use them together:

```python
repository = UserRepository(session)
user = repository.get(
    username_filter(username="python.on.papyrus"),
    AgeGreaterSpecification(age_gt=18),
    JoinSpecification(Friends),
)
```


## SpecificationList
SpecificationList is a static class that contains basic specifications
for our repository.

Specifications:
###### `filter()`
filters the data
###### `order()`
orders the data
###### `paginate()`
paginates the data(limits the results, offsets them).
###### `join()`
joins entities together(join a table, get related data).

The reason we use `SpecificationList` is because we want to have an abstraction for our specifications.
Take two examples:

```python
from dependencies import UserRepository
from assimilator.alchemy.database import alchemy_filter


def get_user(id: int, repository: UserRepository):
    return repository.get(alchemy_filter(id=id)) # we use alchemy_filter() directly 
```
In that example, we use `alchemy_filter()` directly, which may not seem as an issue, however,
if we would want to change our `UserRepository` to work with `RedisRepository`, then we would
have to change all of our specifications ourselves.

In order to fix this, we can use SpecificationList:
```python
from dependencies import UserRepository


def get_user(id: int, repository: UserRepository):
    return repository.get(repository.specifications.filter(id=id))
    # we call the filter from repository specifications. 
```
Now, we only have to change the repository without worrying about other parts of the code.

Here is how you can create your own SpecificationList:

```python
from assimilator.core.database import SpecificationList, specification, Specification
from pagination_func import paginate_data


@specification
def filter_specification(filters, query):
    return query.do_filter(filters)


@specification
def join_specification(query):
    return query    # we do not need joins in our data structure, so we leave it


class OrderSpecification(Specification):
    def __init__(self, orders):
        self.orders = orders

    def apply(self, query):
        return query.make_order(self.orders)


class MySpecificationList(SpecificationList):
    filter = filter_specification  # we use function name as the specification
    order = OrderSpecification  # lambda specification
    paginate = paginate_data  # imported specification
    join = join_specification
```
Notice that we never call the functions, cause the only thing we need are links to the 
specifications.

Then, when you build your Repository:
```python
from specifications import MySpecificationList

repository = MyRepository(session=session, specifications=MySpecificationList)
```
Once you have done that, the repository will use your specifications.

> Of course, you can still use specifications directly, but if you ever need to change
> the repository, then it may be a problem.


## LazyCommand
Sometimes we don't want to execute the query right away. For example, for optimization purposes or 
some other purpose that requires us to delay the execution. In that case, you want to find `lazy` argument
in the function that you are calling and set it to `True`. After that, a `LazyCommand` is going to be returned. That
object allows you to call it as a function or iterate over it to get the results:

```python
from assimilator.core.database import BaseRepository


def print_all_usernames(repository: BaseRepository):
    for user in repository.filter(lazy=True):
        print(user.username)
        # we don't want to receive a list of all the users, but want to iterate
        # through it and only get 1 user at a time


def count_users_if_argument_true(do_count, repository: BaseRepository):
    count_command = repository.count(lazy=True)
    # turn on lazy and get LazyCommand

    if do_count:
        return count_command()  # call for the result
    return -1

```


## Unit of Work
Unit of work allows us to work with transactions and repositories that change the data.
The problem with repository is the transaction management. We want to make our transaction management
as easy as possible, but repositories are not responsible for that. That is why we
have units of work.

They allow us to do the following:
1. Start the transaction
2. Provide the repository to the client code
3. If there are exceptions, errors, issues with the client code, rollback the transaction and remove all the changes
4. If everything is good, the client code calls the `commit()` function and finishes the data change
5. Unit of work closes the transaction


###### `__init__()`

- `repository: BaseRepository` - The repository is provided in the UnitOfWork when we create it. The session
to the data storage is going to be taken from the repository.

###### `begin()`
Starts the transaction. The function is called automatically.

###### `rollback()`
Removes all the changes from the transaction. You do not need to call that function,
as it is called automatically if there is an error in your code.

###### `commit()`
Saves the changes to the data storage. While the repository only adds the temporary, this
function is responsible for the final save. _You need to call it yourself, it will not be called automatically like rollback()_ 

###### `close()`
Closes the transaction. The function is called automatically.


#### Here is how you can use UnitOfWork in your code: 

```python
from assimilator.core.database import UnitOfWork

from users.unit_of_work import UserUnitOfWork
from users.models import User

def create_user(username: str, uow: UnitOfWork):
    with uow:   # start the transaction
        # everything in here is within the transaction
        new_user = User(username=username)
        uow.repository.save(new_user)   # we get the repository from UnitOfWork

        uow.commit()    # commit the changes making them final. If the function is not called, nothing is saved.
```

As you can see, you do not need to call any function except for `commit()`. You should
also use context managers(`with uow:`) to start the transaction and rollback if there is an exception:

```python
from assimilator.core.database import UnitOfWork

from users.unit_of_work import UserUnitOfWork
from users.models import User

def create_user(username: str, uow: UnitOfWork):
    with uow:   # start the transaction
        # everything in here is within the transaction
        new_user = User(username=username)
        uow.repository.save(new_user)   # we get the repository from UnitOfWork

        1 / 0   # ZeroDivisionError. UnitOfWork calls rollback automatically.
        uow.commit()    # nothing is saved, since the rollback was called.
```
