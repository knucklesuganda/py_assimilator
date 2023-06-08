## PyAssimilator Usability Update(1.2.5)

We are focusing on the usability of the library, allowing you to create and manage patterns more comfortably.

##### Problem
You can easily use the patterns, but, it can be hard to setup all of them if you have never worked with PyAssimilator before. For example, if you want to use pattern substitution(change the database without changing your code), then it can be hard to manage all the models for different databases. Example of this can be seen here: https://github.com/knucklesuganda/py_assimilator/blob/master/examples/simple_database/models.py

-------------------------------------------------

##### Solution
We are going to have a registry that is going to contain all patterns with different providers(SQLAlchemy, Redis, etc.). You are going to access that registry with special functions like this:
repository = create_repository(provider='alchemy', model=User, connection=session())
crud = create_crud(provider='mongo', model=Product, connection=MongoClient())


Most of the patterns are going to be created like this. We will also have a model registry for the same purpose, but the implementation is not known yet. 
