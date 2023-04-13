## Adaptive specifications

While working with different queries, you are going to use specifications. However, accessing them from repository can
be challenging. That is why we created Adaptive Specifications. Here is what they do:

That is the code from PyAssimilator version 1.1.0:

```Python
from assimilator.core.database import Repository


def filter_users(repository: Repository):
    return repository.filter(
        repository.specs.filter(
            age__gt=18,
        ),
        repository.specs.join(
            "balances",
            "balances.currency",
        ),
        repository.specs.only(
            "balances.currency.symbol",
            "balances.amount",
        ),
        repository.specs.paginate(
            limit=10,
            offset=18,
        )
    )
```

Here is that same code using 1.2.0 Adaptive Specifications:

```Python
from assimilator.core.database import Repository, only, join, filter_, paginate


def filter_users(repository: Repository):
    return repository.filter(
        filter_(age__gt=18),
        join("balances", "balances.currency"),
        only("balances.currency.symbol", "balances.amount"),
        paginate(limit=10, offset=18),
    )
```

We removed more than 30% of our code! These specifications are going to change depending on your repository, so that
means that you can write them like that and use pattern substitution easily!


## Specification Fixes

We fixed all the specifications that relate to foreign keys. Now, you can easily use `order()` specification with foreign
values:

```Python
# Order by foreign entity `balances` and `amount` column
order('balances.amount')

# Or using specification from the repository
repository.specs.order('balances.amount')
```

We also fixed all the composite filter specification operations:

```Python
# Filter AND filter OR NOT filter
repository.specs.filter(...) & repository.specs.filter(...) | ~repository.specs.filter(...)

# They also work with adaptive specifications!
filter_(...) & filter_(...) | ~filter_(...)
```


## Specification refactoring

Now, we don't use `apply()` function in `Specification` class, we just call `__call__()` straight away.


## Other minor fixes

- Better imports
- Better type hints
- Quicker internal filters
