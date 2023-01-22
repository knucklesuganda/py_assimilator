from typing import Callable, Dict, Tuple


class FilteringOptions:
    def __init__(self):
        self.filter_options: Dict[str, Callable] = {
            "__eq": self._eq,
            "__gt": self._gt,
            "__gte": self._gte,
            "__lt": self._lt,
            "__lte": self._lte,
            "__not": self._not,
            "__is": self._is,
            "__like": self._like,
            "__regex": self._regex,
        }

    def get_default_filter(self) -> Tuple[str, Callable]:
        return '__eq', self._eq

    def parse_filter(self, raw_filter: str) -> Tuple[str, Callable]:
        for filter_ending, filter_func in self.filter_options.items():
            if raw_filter.endswith(filter_ending):
                return filter_ending, filter_func

        return self.get_default_filter()

    def _eq(self, field: str, value):
        raise NotImplementedError("_eq() is not implemented in the filtering options")

    def _gt(self, field: str, value):
        raise NotImplementedError("_gt() is not implemented in the filtering options")

    def _gte(self, field: str, value):
        raise NotImplementedError("_gte() is not implemented in the filtering options")

    def _lt(self, field: str, value):
        raise NotImplementedError("_lt() is not implemented in the filtering options")

    def _lte(self, field: str, value):
        raise NotImplementedError("_lte() is not implemented in the filtering options")

    def _not(self, field: str, value):
        raise NotImplementedError("_not() is not implemented in the filtering options")

    def _is(self, field: str, value):
        raise NotImplementedError("_is() is not implemented in the filtering options")

    def _like(self, field: str, value):
        raise NotImplementedError("_like() is not implemented in the filtering options")

    def _regex(self, field: str, value):
        raise NotImplementedError("_regex() is not implemented in the filtering options")


__all__ = ['FilteringOptions']
