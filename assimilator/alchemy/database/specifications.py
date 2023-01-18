from typing import Collection, Optional

from sqlalchemy.orm import Query
from sqlalchemy.sql.operators import is_
from sqlalchemy import not_, column, desc

from assimilator.core.database.specifications import specification, SpecificationList


@specification
def alchemy_filter(*filters, query: Query, **filters_by) -> Query:
    filters = list(filters)
    removed_filters_by = []

    for field, value in filters_by.items():
        if field.endswith("__gt"):
            filter_ = column(field.replace("__gt", "")) > value
        elif field.endswith("__gte"):
            filter_ = column(field.replace("__gte", "")) >= value
        elif field.endswith("__lt"):
            filter_ = column(field.replace("__lt", "")) < value
        elif field.endswith("__lte"):
            filter_ = column(field.replace("__lte", "")) <= value
        elif field.endswith("__not"):
            filter_ = not_(column(field.replace("__not", "")))
        elif field.endswith("__is"):
            filter_ = is_(column(field.replace("__is", "")))
        else:
            continue

        filters.append(filter_)
        removed_filters_by.append(field)

    for removed_filter in removed_filters_by:
        del filters_by[removed_filter]

    return query.filter(*filters).filter_by(**filters_by)


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
def alchemy_paginate(
    *,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    query: Query,
) -> Query:

    if limit is not None:
        query = query.limit(limit)
    if offset is not None:
        query = query.offset(offset)

    return query


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
    'alchemy_filter',
    'alchemy_order',
    'alchemy_paginate',
    'alchemy_join',
]
