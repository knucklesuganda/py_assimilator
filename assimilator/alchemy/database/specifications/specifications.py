from itertools import zip_longest
from typing import Collection, Optional, Iterable

from sqlalchemy.orm import Query, load_only
from sqlalchemy import column, desc, and_, or_, not_

from assimilator.alchemy.database.specifications.filtering_options import AlchemyFilteringOptions
from assimilator.core.database.specifications import (
    specification,
    SpecificationList,
    SpecificationType,
    FilterSpecification,
)


class AlchemyFilter(FilterSpecification):
    filtering_options_cls = AlchemyFilteringOptions

    def __or__(self, other: 'AlchemyFilter') -> SpecificationType:
        return AlchemyFilter(or_(*self.filters, *other.filters))

    def __and__(self, other: 'AlchemyFilter') -> SpecificationType:
        return AlchemyFilter(and_(*self.filters, *other.filters))

    def __invert__(self):
        return AlchemyFilter(not_(*self.filters))

    def apply(self, query: Query) -> Query:
        return query.filter(*self.filters)


alchemy_filter = AlchemyFilter  # TODO: for old versions support, delete later


@specification
def alchemy_order(*clauses: str, query: Query) -> Query:
    parsed_clauses = []

    for clause in clauses:
        if clause.startswith("-"):
            parsed_clauses.append(desc(column(clause[1:])))
        else:
            parsed_clauses.append(clause)

    return query.order_by(*parsed_clauses)


@specification
def alchemy_paginate(*, limit: Optional[int] = None, offset: Optional[int] = None, query: Query) -> Query:
    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)

    return query


@specification
def alchemy_join(*targets: Collection, query: Query, **join_args: dict) -> Query:
    for target, join_data in zip_longest(targets, join_args, fillvalue=dict()):
        if target is not None:
            query = query.join(target, **join_data)

    return query


@specification
def alchemy_only(*only_fields: Iterable[str], query: Query):
    return query.options(load_only(*(only_field for only_field in only_fields)))


class AlchemySpecificationList(SpecificationList):
    filter = AlchemyFilter
    order = alchemy_order
    paginate = alchemy_paginate
    join = alchemy_join
    only = alchemy_only


__all__ = [
    'AlchemySpecificationList',
    'alchemy_filter',   # TODO: remove in future versions
    'AlchemyFilter',
    'alchemy_order',
    'alchemy_paginate',
    'alchemy_join',
    'alchemy_only',
]
