from typing import List, Iterable, Any, Union, Optional

from assimilator.internal.database.models import InternalModel
from assimilator.core.database import specification, SpecificationList
from assimilator.internal.database.specifications.filter_specifications import InternalFilter

QueryT = Union[str, List[InternalModel]]

internal_filter = InternalFilter    # TODO: remove in later versions


@specification
def internal_order(*args, query: QueryT, **kwargs) -> Iterable[InternalModel]:
    if isinstance(query, str):
        return query

    query = list(query)
    fields = (*args, *kwargs.keys())

    if not any(field.startswith("-") for field in fields):
        query.sort(key=lambda item: [getattr(item, argument) for argument in fields])
        return query

    for field in fields:
        reverse = field.startswith("-")
        query.sort(key=lambda item: getattr(item, field.strip("-")), reverse=reverse)

    return query


@specification
def internal_paginate(
    *,
    query: QueryT,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Iterable[InternalModel]:
    if isinstance(query, str):
        return query

    query = list(query)
    return query[offset:limit]


@specification
def internal_join(*args, query: QueryT, **kwargs) -> Any:
    return query


@specification
def internal_only(*only_fields: Iterable[str], query: QueryT):
    if isinstance(query, str):
        return query

    only_fields = set(only_fields)
    return [model.copy(include=only_fields) for model in query]


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
