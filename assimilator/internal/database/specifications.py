import operator
from typing import List, Iterable, Any, Union, Callable, Optional

from assimilator.core.database import specification, SpecificationList, filter_parameter_parser
from assimilator.internal.database.models import InternalModel


QueryT = Union[str, List[InternalModel]]
internal_filter_mappings = {
    "__gt": lambda field, value: operator.gt,
    "__gte": lambda field, value: operator.ge,
    "__lt": lambda field, value: operator.lt,
    "__lte": lambda field, value: operator.le,
    "__not": lambda field, value: operator.not_,
    "__is": lambda field, value: operator.is_,
}


@specification
def internal_filter(*filters, query: QueryT, **filters_by) -> Iterable[InternalModel]:
    if not (filters_by or filters):  # no filters present
        return query
    elif isinstance(query, str):
        id_ = filters_by.get('id')
        return f'{query}{"".join(filters)}{id_ if id_ else ""}'

    parsed_arguments: List[(str, Callable, Any)] = []

    for field, value in dict(filters_by).items():
        ending, parsed_filter = filter_parameter_parser(
            field=field,
            value=value,
            filter_mappings=internal_filter_mappings,
        )

        parsed_arguments.append((
            field.replace(ending, "") if (ending is not None) else field,
            parsed_filter or operator.eq,
            value,
        ))

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
