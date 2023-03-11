# Database patterns


## What patterns do we use?
Database, in our case, is any data storage. It can be PostgreSQL, MySQL, Redis, File, external API or others. We use
5 main patterns with databases:

- `Repository` - works with the data. Saves, reads, updates, deletes, modifies, checks, filters our data.
- `UnitOfWork` - works with transactions. Ensures data integrity. Only used when the data is changed.
- `Specification` - some sort of filter for the repository. Filters, paginates, joins, limits the results in `Repository`.
- `SpecificationList` - contains links to `Specification` patterns to completely remove imports inside of `Repository`.
- `LazyCommand` - database query that has been created, but not ran yet. Only runs the function when we need the results.

-------------------

## Create/Read example😀

Let's say that we use `SQLAlchemy` library in Python. We want to make a program that can save and read our users.
Each user has a username and balance. The first thing that we do is we need to create SQLAlchemy tables. *There is no
Assimilator in that step*.


```Python
# models.py
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(url="sqlite:///:memory:")    # create engine to the SQLite Database
Base = declarative_base()   # Create a base class for our tables
DatabaseSession = sessionmaker(bind=engine)     # create a database connection(session)


class User(Base):    # Create user model
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    username = Column(String())     # username column
    balance = Column(Float())       # balance column


Base.metadata.create_all(engine)    # Create User table in the database!
```

Most of you have probably seen that. We just create a new SQLAlchemy model in our project.
Now, let's add our Assimilator patterns. Two patterns that we are going to use are `Repository` and `UnitOfWork`.

`Repository` is responsible for data management. We use it to save, read, update, delete, modify, check and basically work with our database.

`UnitOfWork` is responsible for transactions. We use it to apply the changes made by `Repository`.

```Python
# dependencies.py

# We import our patterns from alchemy submodule
from assimilator.alchemy.database import AlchemyUnitOfWork, AlchemyRepository

# We also import User and DatabaseSession we created before 
from models import DatabaseSession, User

user_repository = AlchemyRepository(
    session=DatabaseSession(),
    model=User,
) # We create our repository and pass session and model to it

# UnitOfWork just gets the repository pattern inside it.
user_uow = AlchemyUnitOfWork(repository=user_repository)

```

Now, we will use those patterns to create a user. We need to do the following things:

- Start a new transaction using `UnitOfWork`.
- Create new user using `Repository`.
- Apply the changes using `UnitOfWork`.

The main idea here is that even if we create millions of users, the changes will not be applied to the database until
`UnitOfWork.commit()` function is called. We do that so that if there is an error during our operations, new changes
are not applied.

If you still don't get the idea of database transactions - [watch this video on my channel](https://www.youtube.com/watch?v=E8RoCAp1JSA).

```Python
from assimilator.core.database import UnitOfWork
from dependencies import user_repository, user_uow


def create_user(uow: UnitOfWork):
    with uow:   # We use that to start the transaction
        repository = uow.repository   # access the repository from the UnitOfWork

        # Save the user using Repository.save() function and by passing all the arguments inside
        new_user = repository.save(username="Andrey", balance=1000)

        # WARNING!!! We have not applied any changes up to that point.
        # We must call UnitOfWork.commit() to change that: 
        uow.commit() 
        # Changes are applied and used is in the database!

    return new_user

created_user = create_user(user_uow)
```

We saved the user in the database. Now, let's read it. We use `Specification` pattern to limit the results using different
criteria. If we want to filter the results(SQL WHERE), then we must use `filter()` specification. We can either import
the specifications from the alchemy submodule, or we can access them from the `Repository.specs` property.

> When you are sure that your function is only going to read your database, then you should only use Repository pattern
> without UnitOfWork. This way, we will not commit any data to our database, and can be sure that the function only
> reads the data, without changing it.

```Python
from assimilator.core.database import Repository
from dependencies import user_repository


def get_user(repository: Repository):    # only pass the Repository because we want to read the data
    return repository.get(  # use get() to query one user from the database
        repository.specs.filter(    # use filter specification to give your filtering criteria
            username="Andrey",
        )
    )

user = get_user(user_repository)
```

If you want to import the specification:
```Python
from assimilator.core.database import Repository
from assimilator.alchemy.database import AlchemyFilter  # import AlchemyFilter specification
from dependencies import user_repository


def get_user(repository: Repository):
    return repository.get(
        AlchemyFilter(  # everything else is the same except for the specification
            username="Andrey",
        )
    )

user = get_user(user_repository)
```

As you probably know, those were direct and indirect coding styles. You can read about them [here](/tutorial/important/#indirect-vs-direct-code).
We would suggest you to use indirect(the first) coding style. You remove a lot of imports and can do pattern substitutions which are going to be
discussed in the next example.

-------------------

## Pattern substitution example🙂

What is pattern substitution? It is a technique where you can change the external providers in one step. Let's see what that means...

1. When we write code, it is a good idea to not have dependencies. They are really hard to get rid of, hard to update or change. So,
if we have as little dependencies as possible, this is only going to be better.
2. Sometimes we want to change our database to another one, or we want to change the ORM(database library) that we are using.
3. There is a possibility that we need caching in our program, our we want to run tests of our code without using a real database.

All these examples are perfect for pattern substitution. For that case, we will change SQLAlchemy patterns that we wrote in the
first example to Internal patterns with one line of code.

> Internal patterns work with Python data structures. Your database is a dictionary, list, class or anything else
> within your program. Internal patterns are really useful for testing!

The first thing that we need to do is change the models in our `models.py` file:
```Python
# models.py

from assimilator.core.database import BaseModel     # BaseModel is just a Pydantic model with id


class User(BaseModel):  # id is supplied by default
    username: str
    balance: float

```

So, we changed our SQLAlchemy models to a `BaseModel`. Then, we need to change the patterns:

```Python
# dependencies.py

# We import the same patterns from internal submodule
from assimilator.internal.database import InternalRepository, InternalUnitOfWork
 
from models import User     # import our BaseModel User

# Session is a dictionary in InternalRepository.
# That means, that we will store all our data in there.
session = {}

# We create our repository and pass session and model to it
user_repository = InternalRepository(session=session, model=User)

# UnitOfWork just gets the repository pattern inside it.
user_uow = InternalUnitOfWork(repository=user_repository)

```

That's it. After you changed that, your other code like `create_user()` and `get_user()` will work with dictionary and
your new `User` as a data storage! Now, imagine that you have 200 functions, and in order to change one data storage to
another you just need 1 line of code!


### About direct coding
All of that magic with pattern substitution was possible because we used indirect coding. But, if we use direct coding,
the situation may not be that sweet:

```Python
from assimilator.core.database import Repository
from assimilator.alchemy.database import AlchemyFilter  # import AlchemyFilter specification
from dependencies import user_repository


def get_user(repository: Repository):
    return repository.get(
        AlchemyFilter(
            # We use AlchemyFilter with InternalRepository.
            # Those do not work together😭
            username="Andrey",
        )
    )

user = get_user(user_repository)
```

`AlchemyFilter` will not work with `InternalRepository`. We must go into our code and change it to `InternalFilter`.
That is why we advise you to use indirect coding whenever possible.

-------------------

## Errors example😰

We have already seen perfect examples of working code. But, errors and exceptions happen! That is why we need to ensure
that the code that we write is error-proof.

**However, we have already done everything to do that😳.**

As I said earlier, `UnitOfWork` pattern is used for transaction management. That means, that we use it to commit the data
if everything is OK, or rollback the changes if there are errors. When we use context managers(`with uow`) with `UnitOfWork` pattern
we make it so that if there are errors, all the pending changes are dropped.

So, if you want to add try and except to your code, then just do it like this:

```Python
from assimilator.core.database import UnitOfWork, InvalidQueryError
from dependencies import user_repository, user_uow


def create_user(uow: UnitOfWork):
    try:
        with uow:   # We use that to start the transaction
            repository = uow.repository
            new_user = repository.save(username="Andrey", balance=1000) 
            uow.commit() 

        return new_user

    except InvalidQueryError:
        print("Error in user creation")
        return None     # no user created

created_user = create_user(user_uow)
```

But, even if you do not use try and except, you are sure that your database does not have any weird changes in it!
That's the power of `UnitOfWork`.

> If you ever want to rollback yourself, then use UnitOfWork.rollback() function. It will remove all the pending changes.
> That is the function that is called if there is an exception in the `with uow` block.

-------------------

## Other functions you must know

Here are more short examples regarding Database functions that you might want to use:

### Data querying

```Python
from assimilator.core.database import Repository

def example(repository: Repository):
    repository.get()    # get one entity from the database
    # get() function can raise NotFoundError() or MultipleResultsError()

    repository.filter()    # get many entities from the database
    
    # When you use those functions, you can add specifications to limit the results:
    
    adult_users = repository.filter(
        repository.specs.filter(    # we use filter specification
            age__gte=18,    # get all the users older than 18 years
        )
    )
    
    for adult_user in adult_users:
        print(adult_user.username)

```
There are different filtering options inside of filter() specification:

- `__eq` = equal to. You can omit it and just use `field=value` as we did before
- `__gt` = greater than. Example: `age__gt=18 == (age > 18)`
- `__gte` = greater than equals. Example: `age__gte=18 == (age >= 18)`
- `__lt` = lower than. Example: `age__lt=18 == (age < 18)`
- `__lte` = lower than equals. Example: `age__lte=18 == (age <= 18)`
- `__not` = not equal. Example: `age__not=18 == (age != 18)`
- `__is` = is True or False. Example: `validated__is=True == (validated is True)`
- `__like` = like SQL expression. Converted to regex if not supported. Example: `username__like="Andrey%" == all usernames that start with Andrey`
- `__regex` = regular expression. Example: `username__regex="[1-3]+And.rey\w+" == regular expression, what is there to explain? `

You can use these options like that:
```Python
from assimilator.core.database import Repository


def filter_example(repository: Repository):
    # Get all users between ages 18 to 25 with username
    # that has "And" inside and those who are validated.
    repository.filter(
        repository.specs.filter(
            age__gt=18,
            age__lt=25,
            username__like="%And%",
            validated__is=True,
        )
    )
```

All the users can be queried with `Repository.filter()` without any specifications:
```Python
from assimilator.core.database import Repository

def get_all_users(repository: Repository):
    all_users = repository.filter()     # get all users from the database
```

Pagination is added with `paginate()` specification:
```Python
from assimilator.core.database import Repository


def paginate(repository: Repository):
    paginated_users = repository.filter(
        repository.specs.paginate(
            limit=10,   # limit the results by 10
            offset=20,  # offset the results by 20
        ),
    )
```

Ordering is added with `order()` specification:
```Python
from assimilator.core.database import Repository


def order(repository: Repository):
    ordered_users = repository.filter(
        repository.specs.order(
            'username', # order users by username(Ascending ordering)
            '-balance', # second order of the users is balance(descending order)
        )
    )
    # - in front means descending
```

Entity joins are added with `join()` specification:
```Python
from assimilator.core.database import Repository


def join_example(repository: Repository):
    users_with_products = repository.filter(
        repository.specs.join(
            'orders',    # indirect join with user
            User.products,      # direct join with products
        )
    )
```

If you want to optimize your queries, you can do so by using `only()`. It will accept fields that will be the only
ones on your model:
```Python
from assimilator.core.database import Repository

def only_example(repository: Repository):
    users_with_products = repository.filter(
        repository.specs.only('id', 'username')
        # We only query `id` and `username` from the database. 
        # That reduces results size and query execution time
    )
```

If you want to count something, you can use `count()`:
```Python
from assimilator.core.database import Repository

def count_example(repository: Repository):
    users_count: int = repository.count()    # Count all users
    other_users_count: int = repository.count(
        repository.specs.filter(id__gt=10)    # Count all users with id > 10
    )
```

Sometimes you want to check if your object was updated or not. You can use `is_modified()`:
```Python
is_modified: bool = repository.is_modified(user)
```

---------------
### Lazy evaluation😴

Let's say that you want to load all the users from your table. But, the thing is, you don't need to use them straight away.
Maybe, you want to return the result to another function, or set it as an attribute of an object. If you use the patterns that
we gave you, then your code is going to be clean, but memory-heavy.

To avoid that, you can prepare your function to be executed
with another pattern called `LazyCommand`. It saves the function and all the arguments that you want to provide, and executes it
only when you need it!

You can add lazy=True to enable it in your `Repository`:
```Python
from assimilator.core.database import Repository


def example(repository: Repository):
    # Executes on the spot
    users_list = repository.filter()

    # Creates a lazy command that can be executed later
    users_filter_lazy_command = repository.filter(lazy=True)
```

Now, we can optimize our program like this:
```Python
from typing import List

from assimilator.core.database import Repository, LazyCommand
from dependencies import User, user_repository


# We use typing for LazyCommand and show that it returns a list of Users
def caller(repository: Repository) -> LazyCommand[List[User]]:
    return repository.filter(
        repository.specs.filter(age__gt=18),
        lazy=True,      # make it lazy
    )


def second_function():
    return caller(user_repository)      # Database query not executed yet 


def first_function():
    results = second_function()
    
    # Execute more code...
    
    for user in results:    # The query is executed here
        ...
```
We can optimize our code drastically. Now, we will only make the queries whenever we need them!

> But, if your query returns an error, that error is returned to the query execution, not creation! That is going
> to be `first_function()` in our case. Be sure to handle exceptions in the right place.

Here are the places when your command is executed:
```Python
from assimilator.core.database import Repository, LazyCommand

def lazy_command_execution(repository: Repository):
    lazy_command: LazyCommand = repository.filter(lazy=True)
    
    if lazy_command: # query is executed in boolean statements
        print("Executed!")

    for data in lazy_command:   # query is executed in iterators
        print("Executed!")
    
    lazy_user: LazyCommand = repository.get(repository.specs.filter(id=1))
    print("Executed for User id:", lazy_user.id)    # attribute access execution

    print(lazy_user > 10)   # Boolean execution
```

Another **important** thing about LazyCommand is its execution policy. The thing is that if you use the same `LazyCommand`
object many times, the command is only going to be executed once. This code only runs the query once:
```Python
lazy_command_obj()  # command executed
lazy_command_obj()
lazy_command_obj()
lazy_command_obj()
lazy_command_obj()  # the same result in every other call
```

Another **__FAR MORE IMPORTANT__** thing is the return type of your `LazyCommand`. If you call `Repository.filter()`, it's
going to be an Iterable. If you use `Repository.get()`, it is just one entity. We suggest you add types with Python typings:

```Python
from typing import List

from assimilator.core.database import Repository, LazyCommand
from dependencies import User

def lazy_type_example(repository: Repository):
    lazy_command_many: LazyCommand[List[User]] = repository.filter(lazy=True)
    lazy_command_obj: LazyCommand[User] = repository.get(lazy=True)

    # Now we know what is returned when the command is executed:    
    users: List[User] = lazy_command_many()
    one_user: User = lazy_command_obj()
```

The last thing is building your own `LazyCommand` objects:
```Python
from assimilator.core.patterns import LazyCommand


def func(a, b, c):
    return a + b + c


command: LazyCommand[int] = LazyCommand(
    command=func,   # NOT func()
    a=1, b=2, c=3,  # function arguments
)

assert command == 1 + 2 + 3
```

Also, you can use the decorator to make your whole function lazy:
```Python
from assimilator.core.patterns import LazyCommand


@LazyCommand.decorate
def decorated_lazy(a, b, c):
    return a + b + c


print(decorated_lazy(1, 2, 3))  # 6
print(decorated_lazy(1, 2, 3, lazy=True))  # LazyCommand
```


### More on filter specification
You have probably wondered how to do OR statement in the filter specification. What about AND statement? How are we going to
implement all these things without using direct coding? You can use special operations like these:

```Python

# OR operation. username=="Andrey" or username=="Python":
repository.specs.filter(username="Andrey") | repository.specs.filter(username="Python")


# AND operation. username=="Andrey" and age==22:
repository.specs.filter(username="Andrey") & repository.specs.filter(age=22)

# AND operation, but shorter:
repository.specs.fitler(username="Andrey", age=22)

# NOT operation. age != 55
~repository.specs.filter(age=55)


# Combining operations together.
# (username="Andrey" and age=22) or (username == "Python" and age > 18)
repository.specs.filter(username="Andrey", age=22) | \
repository.specs.filter(username="Python") & \
!repository.specs.filter(age__gt=18) 

```
Another question that you probably have is how to make all of that shorter. Writing the specification again and again
can be tiring. Good thing you can save them(not only filter specification. Any specification in general):
```python
andrey_username_spec = repository.specs.filter(username="Andrey")

andrey = repository.filter(andrey_username_spec)
```


### 🤩New Adaptive Specifications!🤩

What is adaptive specification? It is a function that you can call without accessing `repository.specs`. You can
do it like this:

```Python
# Import adaptive specifications
from assimilator.core.database import filter_, join, order, only, paginate, Repository


def read_users(repository: Repository):
    return repository.filter(
        filter_(username__like="%Andrey%"),
        join("balances"),
        only("username", "balances.amount"),
        paginate(limit=10),
        order("balances.amount"),
    )


```



---------------
### Data changes
Let's finally change some data.
Repository `save()` function can be used with arguments or provided model:

```Python

repository.save(   # indirect method.
    username="Andrey",
    balance=1000,
)
# OR
user = User(username="Andrey", balance=1000)
repository.save(user)  # direct method.
```

Repository `update()` function can be used to update models:
```Python
user = repository.get(repository.specs.limit(limit=1))
user.balance += 100
repository.update(user)    # update the user
```

It can also be used to update a lot of entities at once:
```Python
repository.update(
    # you provide specifications to filter the results
    repository.specs.filter(age__gt=18),
    repository.specs.limit(limit=100),

    # then, you provide field=new_value pairs to update the fields
    is_validated=False,
    updated_field="New value",
)
```

Use `delete()` to delete one model:
```Python
repository.delete(user)
```

Or many models at once:
```Python
repository.delete(  # delete everyone under 18
    repository.specs.filter(age__lt=18)
)
```

> `delete()` is partially safe. That means that you cannot delete your whole database, cause if you provide nothing, you
> will delete nothing. But, still check your specifications in mass delete statements.


Use `refresh()` to update the values in your old object. It goes to the database and changes your old values to new if they
were updated:
```Python
repository.refresh(old_user)
assert old_user.updated_field == repository.get(repository.specs.filter(id=old_user.id)).updated_field
```


-------------------

## Typical flows

### Data Creation

1) You create Repository and UnitOfWork.

```Python
from assimilator.alchemy.database import AlchemyRepository, AlchemyUnitOfWork

user_repository = AlchemyRepository(
    session=DatabaseSession(),  # your SQLAlchemy session
    model=User,         # User is your SQLAlchemy model
)
user_uow = AlchemyUnitOfWork(repository=user_repository)
```

2) You provide them in the function as parameters.

```Python
from assimilator.core.database import UnitOfWork

def create_user(new_username: str, uow: UnitOfWork): ...    # UnitOfWork is a parameter
```

3) You use context manager(with statement in Python) with UnitOfWork.

```Python

def create_user(new_username: str, uow: UnitOfWork):
    with uow:      # Start the transaction in the database
        ...

```

4) You get the repository from UnitOfWork and use `save()` to save the result.

```Python

def create_user(new_username: str, uow: UnitOfWork):
    with uow:
        new_user = uow.repository.save(
            username=new_username,
            user_balance=0,
        )  # create new user

```

5) You use UnitOfWork `commit()` to apply the changes to the database.

```Python

def create_user(new_username: str, uow: UnitOfWork):
    with uow:
        new_user = uow.repository.save(
            username=new_username, 
            user_balance=0,
        )  # create new user
        uow.commit()    # Save changes do the database

    return new_user     # return new user

```

-----------------------------------------------

### Data Filtering

1) You create Repository.

```Python
from assimilator.alchemy.database import AlchemyRepository

user_repository = AlchemyRepository(
    session=DatabaseSession(),  # your SQLAlchemy session
    model=User,         # User is your SQLAlchemy model
)
```

2) You provide it in the function as a parameter.

```Python
from assimilator.core.database import Repository

def filter_users(age: int, repository: Repository): ...    # Repository is a parameter
```

3) You use Repository `filter()` function to filter the results.

```Python

def filter_users(age: int, repository: Repository):
    return repository.filter(...)

```

4) You use `repository.specs` to access the specifications. Then, you choose filter to filter the users who are
18 or older:

```Python

def filter_users(age: int, repository: Repository):
    return repository.filter(
        repository.specs.filter(age__gte=18)     # age >= 18
    )

```

5) _Optional step_ You can use direct coding style to use the specification like this:

```Python
from assimilator.alchemy.database import AlchemyFilter

def filter_users(age: int, repository: Repository):
    return repository.filter(
        AlchemyFilter(age__gte=18)     # age >= 18
    )

```

6) _Optional step_ You use direct coding style with SQLAlchemy filter

```Python
from assimilator.alchemy.database import AlchemyFilter

def filter_users(age: int, repository: Repository):
    return repository.filter(
        User.age >= 18     # Your SQLAlchemy User model. age >= 18
    )

```
