import operator
import re
from functools import wraps
from numbers import Number
from typing import Any, Callable, Tuple, Set, List, Union, Literal, Dict

from assimilator.core.database import BaseModel, FILTERING_OPTIONS_SEPARATOR


Containers = (List, Set, Tuple, map)


def find_attribute(func: callable, field: str, value: Any) -> Callable[[BaseModel], bool]:
    """
    That decorator is used to get the value of the field from a BaseModel that is provided in the query.
    We do that because we need to get the value of the field in the internal specifications, not just the name
    of it. For example, User(id=1) will use field='id' to get 1 as the result.

    :param func: filtering option function that is going to be decorated
    :param field: field name that is used in getattr(model, field)
    :param value: value of the field
    :return: function to be called with a model to find an attribute and call the comparison function
    """

    @wraps(func)
    def find_attribute_wrapper(model: BaseModel) -> bool:
        foreign_fields = field.split(FILTERING_OPTIONS_SEPARATOR)

        if len(foreign_fields) == 1:
            return func(getattr(model, foreign_fields[0]), value)

        model_val = model
        for foreign_field in foreign_fields:
            if isinstance(model_val, Containers):
                model_val = list(getattr(obj, foreign_field) for obj in model_val)
            elif isinstance(model_val, Dict):
                model_val = list(getattr(obj, foreign_field) for obj in model_val.values())
            else:
                model_val = getattr(model_val, foreign_field)

        if isinstance(model_val, Containers):
            return any(func(member, value) for member in model_val)

        return func(model_val, value)

    find_attribute_wrapper: func
    return find_attribute_wrapper


def eq(field: str, value: Any):
    return find_attribute(func=operator.eq, field=field, value=value)


def gt(field: str, value: Number):
    return find_attribute(func=operator.gt, field=field, value=value)


def gte(field: str, value: Number):
    return find_attribute(func=operator.ge, field=field, value=value)


def lt(field: str, value: Number):
    return find_attribute(func=operator.lt, field=field, value=value)


def lte(field: str, value: Number):
    return find_attribute(func=operator.le, field=field, value=value)


def not_(field: str, value: Union[Literal[True], Literal[False], Literal[None]]):
    return find_attribute(func=operator.not_, field=field, value=value)


def is_(field: str, value: Union[Literal[True], Literal[False], Literal[None]]):
    return find_attribute(func=operator.is_, field=field, value=value)


def regex(field: str, value: str):
    return find_attribute(
        func=lambda model_val, val: re.compile(value).match(model_val),
        field=field,
        value=value,
    )


def like(field: str, value: str):
    return regex(field, f'^{value.replace("%", ".*?")}$')


__all__ = [
    'find_attribute',
    'eq',
    'gt',
    'gte',
    'lt',
    'lte',
    'not_',
    'is_',
    'regex',
    'like',
]
