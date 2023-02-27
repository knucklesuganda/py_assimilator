# Architecture tutorial

This tutorial will bring up some points on how to create your apps.


## Repository creation

When we create our repositories, we need to provide our model type in the constructor. Let's say that we have a program
with User, Product, Order, UserAddress, Billing entities. Do we create five repositories for each model? Do we only have
one repository for User? It depends.

What you want to do in general is find your primary entities. Primary entity is a model that can live by itself, and does
not add any information to other models. User is a primary entity in the majority of cases, because our users can be stored
by themselves. UserAddress, on the other hand, cannot live without a User that it is bound to. So, there is no need to
create a `Repository` for UserAddress. What you want to do is a new `Repository` for User, and write your code in such
a way that your primary entity manages auxiliary entities. If you want to know more about that, please, read Domain-Driven
design books. PyAssimilator does not follow them maniacally, but they have good basis that we use in here.


## Repository and Unit Of Work synergy

When you want to change your data you are always going to use `UnitOfWork`. You have to make sure that you don't create
any additional repositories in your business logic code. That is, you want to use `UnitOfWork` as your `Repository` source:
`uow.repository`. We do that because we want to remove any kind of dependency from our business logic code, and because we 
don't want to open multiple sessions when we don't need it. 


## Pattern creations

It's better if you create your patterns in separate files and use Dependency Injection to provide them in your business
logic code. Dependency Injections allow you to remove dependencies from your business logic code, and they are very
useful for pattern substitution. There are multiple ways of using them. You could look at the way Django does that with
string imports or find a Dependency Injection framework that can help you with that.
