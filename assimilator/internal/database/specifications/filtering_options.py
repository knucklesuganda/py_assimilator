import re
import operator

from assimilator.core.database.specifications import FilteringOptions


class InternalFilteringOptions(FilteringOptions):
    _eq = operator.eq
    _gt = operator.gt
    _gte = operator.ge
    _lt = operator.lt
    _lte = operator.le
    _not = operator.not_
    _is = operator.is_

    def _like(self, field: str, value):
        return self._regex(field, f'^{value.replace("%", ".*?")}$')

    def _regex(self, field: str, value):
        return re.compile(value).match(field)


__all__ = ['InternalFilteringOptions']
