from typing import Any, Callable

from assimilator.core.database import BaseModel
from assimilator.core.database.specifications import FilteringOptions
from assimilator.internal.database.specifications.internal_operator import (
    find_attribute, eq, gte, gt, lte, lt, is_, not_, like, regex,
)


class InternalFilteringOptions(FilteringOptions):
    def __init__(self, attr_finder: Callable[[Callable, str, Any], Callable[[BaseModel], bool]] = find_attribute):
        super(InternalFilteringOptions, self).__init__()
        self.attr_finder = attr_finder

    _eq = staticmethod(eq)
    _gt = staticmethod(gt)
    _gte = staticmethod(gte)
    _lt = staticmethod(lt)
    _lte = staticmethod(lte)
    _not = staticmethod(not_)
    _is = staticmethod(is_)
    _like = staticmethod(like)
    _regex = staticmethod(regex)


__all__ = [
    'InternalFilteringOptions',
    'find_attribute',
    "eq",
    "gte",
    "gt",
    "lte",
    "lt",
    "is_",
    "not_",
    "like",
    "regex",
]
