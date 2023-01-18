import operator
from typing import List, Iterable, Any, Union, Callable, Optional

from assimilator.core.database import specification, SpecificationList
from assimilator.internal.database.models import InternalModel


QueryT = Union[str, List[InternalModel]]


@specification
def internal_filter(*args, query: QueryT, **kwargs) -> Iterable[InternalModel]:
    if isinstance(query, str):
        return f"{query}{''.join(args)}"
    elif not (kwargs or args):    # no filters present
        return query

    parsed_arguments: List[(str, Callable, Any)] = []

    for field, value in kwargs.items():
        operation = operator.eq

        if field.endswith("__gt"):
            operation = operator.gt
            field = field.replace("__gt", "")
        elif field.endswith("__gte"):
            operation = operator.ge
            field = field.replace("__gte", "")
        elif field.endswith("__lt"):
            operation = operator.lt
            field = field.replace("__lt", "")
        elif field.endswith("__lte"):
            operation = operator.le
            field = field.replace("__lte", "")
        elif field.endswith("__not"):
            operation = operator.not_
            field = field.replace("__not", "")
        elif field.endswith("__is"):
            operation = operator.is_
            field = field.replace("__is", "")

        parsed_arguments.append((field, operation, value))

    return list(filter(
        lambda model: all(
            operation_(getattr(model, field_), val)
            for field_, operation_, val in parsed_arguments
        ),
        query,
    ))


@specification
def internal_order(*args, query: QueryT, **kwargs) -> Iterable[InternalModel]:
    if isinstance(query, str):
        return query

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
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    query: QueryT = None,
) -> Iterable[InternalModel]:
    if query is None:
        raise ValueError("Query must not be None in the specification!")
    if isinstance(query, str):
        return query

    return query[offset:limit]


@specification
def internal_join(*args, query: QueryT, **kwargs) -> Any:
    return query


class InternalSpecificationList(SpecificationList):
    filter = internal_filter
    order = internal_order
    paginate = internal_paginate
    join = internal_join


__all__ = [
    'internal_filter',
    'internal_order',
    'internal_paginate',
    'internal_join',
    'InternalSpecificationList',
]
