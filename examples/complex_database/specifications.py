from assimilator.core.database import specification


@specification
def internal_average_balance_specification(query: list, **_) -> float:
    return sum([
        sum([currency.balance for currency in user.balances])
        for user in query
    ]) / len(query)
