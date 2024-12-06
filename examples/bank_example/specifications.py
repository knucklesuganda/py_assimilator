from sqlalchemy import Select, func, select

from assimilator.core.database import specification
from examples.bank_example.models import UserTransaction


@specification
def transactions_statistics(query: Select, **_) -> Select:
    return select(
        func.avg(UserTransaction.balance_change).label("average_value"),
        func.max(UserTransaction.balance_change).label("max_value"),
        func.min(UserTransaction.balance_change).label("min_value"),
    )
