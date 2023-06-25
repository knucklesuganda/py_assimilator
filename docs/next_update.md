## PyAssimilator Model Singularity Update(1.4.0)

We are focusing on the usability of the library, allowing you to use the same model with different data sources.

##### Problem
You can easily use the same logic with different data sources. Example of that is: use the same code with SQLAlchemy and MongoDB.
But, the problem is that you have to create two models: SQLAlchemy model and MongoDB model in your configurations.
You can see that we create lots of classes in here: https://github.com/knucklesuganda/py_assimilator/blob/master/examples/simple_database/models.py
The logic and structure of these models is the same, but we kind of copy our code.

-------------------------------------------------

##### Solution
We will create a single class/function that will allow us to use the same model class with different providers and libraries.
The implementation is not known yet.
