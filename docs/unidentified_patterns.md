## LazyCommand

`LazyCommand` is an object that allows you to postpone the execution of any kind of code.
You will typically use it in some kind of pattern with `lazy=True` argument. But, if you want to create your own `LazyCommand`, then
you can do it like this:

```Python
from assimilator.core.patterns import LazyCommand


def func(a: int, b: int):
    # Function we want to postpone
    return a + b - 10 * a ** b


lazy_func: LazyCommand[int] = LazyCommand(
    command=func,   # command is the function you want to execute
    a=10,   # argument a
    b=20,    # argument b
)

print("No execution yet")

lazy_func() # function is executed here
```


### Operations

You can do the following things with `LazyCommand`:

```Python
# call it
lazy_func()


# iterate it(if the result is iterable)
for value in lazy_func:
    print(value)


# use it as boolean
if lazy_func:
    print("Result gives True")


# get attributes from the result
print(lazy_obj.obj_attr)


# compare it
lazy_obj > 10
```

### Result retrieval

When we use any of the `LazyCommand` methods, we must run the function for the result. That means, that if we want
to use two methods on the same `LazyCommand` object, we must store the result in a variable not to run calculation twice.

```Python
from assimilator.core.patterns import LazyCommand


lazy_func: LazyCommand[int] = LazyCommand(
    command=run_api_query,    # runs API query
    # no other arguments present
)

print("API result:", lazy_func())   # run_api_query() execution

if lazy_func:   # The result is stored in the LazyCommand, no execution needed
    print("API returned true!")
```

### Decorator

Sometimes you want to make your function lazy, but you don't want to write any additional code for that. If that is the
case, then you can use LazyCommand decorator:

```Python
from assimilator.core.patterns import LazyCommand


@LazyCommand.decorate   # decorate LazyCommand 
def get_user_from_api(
    id: int,
    lazy: bool = False,
):
    ...


# Now, we can run it like this:
lazy_command = get_user_from_api(id=1, lazy=True)

# We can also execute it normally:
user = get_user_from_api(id=1)
```
