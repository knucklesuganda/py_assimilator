import operator
from typing import List, Iterable, Any, Union, Callable

from assimilator.core.database import specification, SpecificationList
from assimilator.internal.database.models import InternalModel


@specification
def internal_filter(*args, query: Union[List[InternalModel], str], **kwargs) -> Iterable[InternalModel]:
    if isinstance(query, str):
        return f"{query}{''.join(args)}"

    if not (kwargs or args):    # no filters present
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

    return filter(
        lambda model: all(
            operation_(getattr(model, field_), val) for field_, operation_, val in parsed_arguments
        ), query,
    )


@specification
def internal_order(*args, query: List[InternalModel], **kwargs) -> Iterable[InternalModel]:
    return sorted(
        query,
        key=lambda item: [getattr(item, argument) for argument in (args, *kwargs.keys())],
    )


@specification
def internal_paginate(limit: int, offset: int, query: List[InternalModel]) -> Iterable[InternalModel]:
    return query[limit:offset]


@specification
def internal_join(*args, query: Any, **kwargs) -> Any:
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
