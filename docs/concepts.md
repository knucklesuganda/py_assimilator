# How do we build these patterns

### 1) Dependency injection
Dependency injection is a really important concept in assimilator. We do
not use any additional dependency injection frameworks, but all the patterns inject 
different components into themselves. [If you want to know more about DI](https://www.youtube.com/watch?v=HFU4nAaU63c&feature=youtu.be)

### 1) SOLID
SOLID principles are highly used in assimilator. That means, that in theory
you can replace one pattern to another and experience no trouble in using them. 
_That is why it is not advised to create your own function in patterns, but you can easily
override them. For example, you don't want to create: createUsers() in Repository pattern, but
can override save() function without any problems_. With that said, it is almost impossible
to write such vast variety of patterns without breaking some of the principles. But, if you have
any ideas on how to fix that, then be sure to check out our [Github](https://github.com/knucklesuganda/py_assimilator)

### 1) Domain-driven design
Most of the patterns here are used in Domain driven design. You do not really need to know all the intricacies, but 
make sure that you know the basics of it.
