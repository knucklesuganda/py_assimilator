# PyAssimilator concepts

We want to write the best code. Our code must use the best techniques that other programmers created, have
no dependencies, and be readable. On the other hand, we don't want to spend a lot of time writing that code, because the
only final measure for our program is **result**.

That is why we use PyAssimilator. What we want to do is create patterns that allow us to remove dependencies from our code
and make it cleaner. Our patterns can either:

1. Talk to a database - `Repository, UnitOfWork`
2. Optimize our code - `LazyCommand, ErrorWrapper`
3. Make it more readable - `CRUDService, Service`
4. Make it more secure - `UnitOfWork`
5. Help other patterns - `Specification, SpecificationList, AdaptiveSpecification`
 
We use these patterns and tick all of the boxes above. That is the whole point of this library. Now, you can start
reading [Basic Tutorials](/tutorial/database/).

-------------------------------------

# How do we build these patterns

You don't really need to read about these concepts below as you will see them later. But, if you want to know all the things
that were put into this library - be free to check out things below!

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
