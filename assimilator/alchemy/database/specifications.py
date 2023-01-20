from typing import Collection, Optional, Iterable

from sqlalchemy.orm import Query, load_only
from sqlalchemy.sql.operators import is_
from sqlalchemy import column, desc

from assimilator.core.database.specifications import specification, SpecificationList,\
    filter_parameter_parser


alchemy_filter_mappings = {
    "__gt": lambda field_, val: column(field_) > val,
    "__gte": lambda field_, val: column(field_) >= val,
    "__lt": lambda field_, val: column(field_) < val,
    "__lte": lambda field_, val: column(field_) <= val,
    "__not": lambda field_, val: column(field_) != val,
    "__is": lambda field_, val: is_(column(field_, val)),
}


@specification
def alchemy_filter(*filters, query: Query, **filters_by) -> Query:
    filters = list(filters)

    for field, value in dict(filters_by).items():
        _, parsed_filter = filter_parameter_parser(
            field=field,
            value=value,
            filter_mappings=alchemy_filter_mappings,
        )

        if parsed_filter is not None:
            filters.append(parsed_filter)
            del filters_by[field]

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


@specification
def alchemy_only(*only_fields: Iterable[str], query: Query):
    return query.options(load_only(*(only_field for only_field in only_fields)))


class AlchemySpecificationList(SpecificationList):
    filter = alchemy_filter
    order = alchemy_order
    paginate = alchemy_paginate
    join = alchemy_join
    only = alchemy_only


__all__ = [
    'AlchemySpecificationList',
    'alchemy_filter',
    'alchemy_order',
    'alchemy_paginate',
    'alchemy_join',
]
