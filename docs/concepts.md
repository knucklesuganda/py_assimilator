# How do we build these patterns

### 1. Dependency injection
Dependency injection is a really important concept in assimilator. We do
not use any additional dependency injection frameworks, but all the patterns inject 
different components into themselves. [If you want to know more about DI](https://www.youtube.com/watch?v=HFU4nAaU63c&feature=youtu.be)

### 2. SOLID
SOLID principles are highly used in assimilator. That means, that in theory
you can replace one pattern to another and experience no trouble in using them. 
_That is why it is not advised to create your own function in patterns, but you can easily
override them. For example, you don't want to create: createUsers() in Repository pattern, but
can override save() function without any problems_. With that said, it is almost impossible
to write such vast variety of patterns without breaking some principles. But, if you have
any ideas on how to fix that, then be sure to check out our [GitHub](https://github.com/knucklesuganda/py_assimilator)

### 3. Domain-driven design
Most of the patterns here are used in Domain driven design. You do not really need to know all the intricacies, but 
make sure that you know the basics of it.


### 4. Reusable patterns
The best thing about our patterns is that you can write your code for SQLAlchemy, then change it to Redis, then change
it to Kafka, and finally test it with Python dictionaries. The thing is, you only have to change your pattern creation 
code, everything else stays the same. All the functions work the same in all the patterns that we create.
