from typing import List, Iterable, Union, Optional, Collection

from assimilator.core.database import specification, SpecificationList, BaseModel
from assimilator.internal.database.specifications.filter_specifications import InternalFilter
from assimilator.internal.database.specifications.utils import find_model_value

QueryT = Union[str, List[BaseModel]]
internal_filter = InternalFilter


def _internal_ordering(sorting_field: str):
    fields = sorting_field.strip("-").split(".")

    def _internal_ordering_wrapper(item: BaseModel):
        current = find_model_value(fields=fields, model=item)

        return current

    return _internal_ordering_wrapper


@specification
def internal_order(*clauses: str, query: QueryT, **_) -> Iterable[BaseModel]:
    if isinstance(query, str):
        return query

    query = list(query)
    for field in clauses:
        query.sort(
            key=_internal_ordering(sorting_field=field),
            reverse=field.startswith("-"),
        )

    return query


@specification
def internal_paginate(
    *,
    query: QueryT,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    **_,
) -> Iterable[BaseModel]:
    if isinstance(query, str):
        return query

    return list(query)[offset:limit]


@specification
def internal_join(*targets: Collection, query: QueryT, **join_args: dict) -> QueryT:
    return query


@specification
def internal_only(*only_fields: Iterable[str], query: QueryT, **_) -> Iterable[BaseModel]:
    """
    This specification will do nothing since we waste more resources trying to remove all the fields.
    Also, we must provide a deference mechanisms for fields to be loaded which is impossible.
    """
    return query


class InternalSpecificationList(SpecificationList):
    filter = internal_filter
    order = internal_order
    paginate = internal_paginate
    join = internal_join
    only = internal_only


__all__ = [
    'internal_filter',
    'InternalFilter',
    'internal_order',
    'internal_paginate',
    'internal_join',
    'internal_only',
    'InternalSpecificationList',
]
