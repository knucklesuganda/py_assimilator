# Important things related to all patterns


## What is a pattern???

Pattern - typical solution to commonly occurring problems. In our case, the problems are:

- Database communication
- Data integrity
- Event-based systems
- Coding speed
- Good code
- External dependencies
- The best code that some people cannot write easily

We solve all of them with different classes like: `Repository`, `UnitOfWork`, `Producer`, and so on. Each
class is a pattern. Lots of them are used with each other: `Repository` is always used with `UnitOfWork` and `Specification`.


## Indirect vs Direct code
When you write your code, you can choose two styles: direct and indirect. What does that mean?
We use different libraries like SQLAlchemy, PyRedis, PyMongo and others to ease the use of our patterns.
We did not want to create a module that allows you to completely remove these modules from your code. 

But, we made it so our patterns are interchangeable. That means that you can write some code for SQLAlchemy, and change
it to Redis 2 minutes later, even if you coded 20 000 lines.

### Indirect coding style
- You do not import any functions from assimilator, every useful thing is directly in the pattern.
- You do not use anything from external providers(except for pattern creation) in your code. You only use our patterns.

Indirect coding example:
```Python
 
def create_user(uow: UnitOfWork):
    with uow:
        uow.repository.save(
            username="Andrey",  # No external library usage
            email="python.on.papyrus@gmail.com",
        )

        
def filter_users(repository: Repository):
    return repository.filter(repository.specs.filter(balance__gt=20))   # only using arguments


# Patterns Configuration
# External library(SQLAlchemy) is only found in the pattern creation
repository = AlchemyRepository(Session(), model=User)
uow = AlchemyUnitOfWork(repository)
```

### Direct coding style
- You import functions and objects from assimilator.
- You use things from external libraries in your code with assimilator patterns

Direct coding example:
```Python
 
def create_user(uow: UnitOfWork):
    with uow:
        new_user = User(    # SQLAlchemy model is used directly
            username="Andrey",  # No external library usage
            email="python.on.papyrus@gmail.com",
        )
        uow.repository.save(new_user)

        
def filter_users(repository: Repository):
    return repository.filter(
        repository.specs.filter(User.balance > 20),   # SQLAlchemy filter user
        # AlchemyFilter(User.balance > 20),   # AlchemyFilter is imported from assimilator, direct use
    )   # repository.specs.filter == AlchemyFilter for AlchemyRepository, but you either use it directly or indirectly


# Patterns Configuration. Everything is the same
repository = AlchemyRepository(Session(), model=User)
uow = AlchemyUnitOfWork(repository)
```

## Why do you need all that?

#### Indirect style pluses ✔️
- You won't have any external dependencies. For example, you don't want to use SQLAlchemy
directly.
- You can change data storages by only changing the configuration:

```Python 
def create_user(uow: UnitOfWork):
    """ Stays the same using indirect coding """

        
def filter_users(repository: Repository):
    """ Stays the same using indirect coding """


# Patterns Configuration
# You can change pattern creation and move to another data storage without any issues.
repository = RedisRepository(Redis(), model=RedisUser)  ####### LOOK HERE
uow = RedisUnitOfWork(repository)
```

#### Indirect minuses ❌

- Indirect coding is a little slower than the direct one.
- It may not include all the features that your app
needs. For example, what if you need to run a MongoDB pipeline with aggregation framework😵(even though you can do this specific thing with indirect coding).

-------------------------------------------

#### Direct style pluses ✔️
- Your app is very complex, and you don't have all the features in indirect variant.
- You are 100% sure that you will not change your code to other external libraries with Assimilator patterns.
- A little faster since we do not parse anything, we just use external objects and methods.

#### Direct minuses ❌

- Very hard to move to other data storages or libraries since you are using external features directly.
- External dependencies in your code.


## How to choose?
We prefer to use indirect style, since it hides dependencies. But, what you need to do is adapt to your project. Start
with indirect style and use direct features only when needed.
