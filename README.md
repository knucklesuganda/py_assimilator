# Assimilator - the best Python patterns for the best projects

<p align="center">
  <a href="https://knucklesuganda.github.io/py_assimilator/"><img src="https://knucklesuganda.github.io/py_assimilator/images/logo.png" alt="PyAssimilator"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/py-assimilator/" target="_blank">
    <img src="https://img.shields.io/github/license/knucklesuganda/py_assimilator?color=%237e56c2&style=for-the-badge" alt="License">
</a>

<a href="https://pypi.org/project/py-assimilator/" target="_blank">
    <img src="https://img.shields.io/github/stars/knucklesuganda/py_assimilator?color=%237e56c2&style=for-the-badge" alt="Stars">
</a>
<a href="https://pypi.org/project/py-assimilator/" target="_blank">
    <img src="https://img.shields.io/github/last-commit/knucklesuganda/py_assimilator?color=%237e56c2&style=for-the-badge" alt="Last commit">
</a>
</p>


## Install now
* `pip install py-assimilator`

## What is that all about?

1. We want to write the best code.
2. We need the best patterns and techniques for this.
3. We use PyAssimilator and save lots of time.
4. We use PyAssimilator and write the best code.
4. We use PyAssimilator and use the best patterns.
6. We use PyAssimilator and have no dependencies in our code.
7. We use PyAssimilator and can switch one database to another in a matter of seconds.
7. We learn PyAssimilator once and use it forever!
7. **And most importantly, we make Python projects better!**


## Code comparison

Before PyAssimilator:
```Python
# BAD CODE :(

def create_user(username: str, email: str):
    # NO PATTERNS!
    # ONLY ONE DATABASE CHOICE!
    new_user = User(username=username, email=email, balance=0) # DEPENDENCY!
    session = db_session()  # DEPENDENCY!
    session.add(new_user)
    session.commit()  # NO ACID TRANSACTIONS!
    return new_user

```

After:
```Python
# GOOD CODE :)

def create_user(username: str, email: str, uow: UnitOfWork):
    # BEST DDD PATTERNS
    # PATTERN SUBSTITUTION/MULTIPLE DATABASES AT ONCE

    with uow:   # ACID TRANSACTIONS IN ANY DATABASE
        new_user = uow.repository.save(
            username=username,  # NO MODEL DEPENDENCIES
            email=email,
            balance=0,
        )
        uow.commit()    # AUTO ROLLBACK

    return new_user

```

## So, do I really need it?

If you want to spend less time writing your code, but write better code - then you must use PyAssimilator.
It can be hard to start if you have no experience with good code, so you can watch creator's [video tutorials](https://knucklesuganda.github.io/py_assimilator/video_tutorials/).


## Our vision

Make Python the best programming language for enterprise development and use all of its dynamic capabilities to write
things that other languages can't even comprehend!

- Pattern substitution(switch databases easily) ✔️
- Event-based patterns(in development) 🛠️
- 45% of all Python projects use PyAssimilator 🛠️
- Independent code(in development) 🛠️
- Adaptive patterns(in development) 🛠️
- Automatic code improvements(in development) 🛠️
- Decentralized code management(in development) 🛠️

If you want to help with any of those things - be free to contribute to the project. Remember, you never do anything for
free - and that will not be the case either.

## Sources
* [Github](https://github.com/knucklesuganda/py_assimilator)
* [PyPI](https://pypi.org/project/py-assimilator/)
* [Documentation](https://knucklesuganda.github.io/py_assimilator/)
* [Github](https://github.com/knucklesuganda/py_assimilator)
* [Author's YouTube RU](https://www.youtube.com/channel/UCSNpJHMOU7FqjD4Ttux0uuw)
* [Author's YouTube ENG](https://www.youtube.com/channel/UCeC9LNDwRP9OfjyOFHaSikA)
* [Discord channel](https://discord.gg/gTVaGu7DHN)

 ## Contributors

<a href="https://github.com/knucklesuganda/py_assimilator/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=knucklesuganda/py_assimilator" />
</a>

## Stars history

[![Star History Chart](https://api.star-history.com/svg?repos=knucklesuganda/py_assimilator&type=Date)](https://star-history.com/#knucklesuganda/py_assimilator&Date)


## ⭐Stargazers⭐

We love all people who star our library. You can look at all stargazers in the documentation:

https://knucklesuganda.github.io/py_assimilator/#stars-history

> If you star the library you will appear there as well!


## Types of patterns
These are different use cases for the patterns implemented:

- Database - patterns for database/data layer interactions.
- Events(in development) - projects with events or event-driven architecture.
- Unidentified - patterns that are useful for different purposes.

## Available providers
Providers are different patterns for external modules like SQLAlchemy or FastAPI.

- Alchemy(Database, Events) - patterns for [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) for both database and events.
- Kafka(Events) - patterns in [Kafka](https://kafka.apache.org/) related to events.
- Internal(Database, Events) - internal is the type of provider that saves everything in memory(dict, list and all the tools within your app).
- Redis(Database, Events) - redis_ allows us to work with [Redis](https://redis.io/) memory database.
- MongoDB(Database) - mongo allows us to work with [MongoDB](https://www.mongodb.com/) database.
