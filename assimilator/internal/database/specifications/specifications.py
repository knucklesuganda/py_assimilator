from typing import List, Iterable, Union, Optional, Collection

from assimilator.core.database import specification, SpecificationList, BaseModel
from assimilator.internal.database.specifications.filter_specifications import InternalFilter

QueryT = Union[str, List[BaseModel]]

internal_filter = InternalFilter    # TODO: remove in later versions


@specification
def internal_order(*clauses, query: QueryT) -> Iterable[BaseModel]:
    if isinstance(query, str):
        return query

    query = list(query)

    if not any(field.startswith("-") for field in clauses):
        query.sort(key=lambda item: [getattr(item, argument) for argument in clauses])
    else:
        for field in clauses:
            query.sort(
                key=lambda item: getattr(item, field.strip("-")),
                reverse=field.startswith("-"),
            )

    return query


@specification
def internal_paginate(
    *,
    query: QueryT,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Iterable[BaseModel]:
    if isinstance(query, str):
        return query

    return list(query)[offset:limit]


@specification
def internal_join(targets: Collection, join_args: Collection[dict], query: QueryT) -> QueryT:
    return query


@specification
def internal_only(*only_fields: Iterable[str], query: QueryT):
    if isinstance(query, str):
        return query

    return [model.copy(include=set(only_fields)) for model in query]


class InternalSpecificationList(SpecificationList):
    filter = internal_filter
    order = internal_order
    paginate = internal_paginate
    join = internal_join
    only = internal_only


__all__ = [
    'internal_filter',
    'internal_order',
    'internal_paginate',
    'internal_join',
    'InternalSpecificationList',
]
