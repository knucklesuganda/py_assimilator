from typing import Iterable, Collection

from sqlalchemy.orm import Query

from assimilator.core.database.specifications import Specification, specification, SpecificationList


class AlchemySpecification(Specification):
    def apply(self, query: Query) -> Query:
        return super(AlchemySpecification, self).apply(query)


@specification
def alchemy_filter(*filters, query: Query, **filters_by) -> Query:
    return query.filter(*filters).filter_by(**filters_by)


@specification
def alchemy_order(*clauses: str, query: Query) -> Query:
    return query.order_by(*clauses)


@specification
def alchemy_paginate(limit: int, offset: int, query: Query) -> Query:
    return query.limit(limit).offset(offset)


@specification
def alchemy_join(targets: Collection, join_args: Collection[dict], query: Query) -> Query:
    if len(join_args) < len(targets):
        join_args += [dict() for _ in range(len(targets) - len(join_args))]

    for target, join_data in zip(targets, join_args):
        query = query.join(target, **join_data)

    return query


class AlchemySpecificationList(SpecificationList):
    filter = alchemy_filter
    order = alchemy_order
    paginate = alchemy_paginate
    join = alchemy_join


__all__ = [
    'AlchemySpecificationList',
    'AlchemySpecification',
    'alchemy_filter',
    'alchemy_order',
    'alchemy_paginate',
    'alchemy_join',
]
