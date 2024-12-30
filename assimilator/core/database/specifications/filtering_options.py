from typing import Any, Callable, Dict, Protocol


class FilterOptionProtocol(Protocol):
    def __call__(self, field: str, value: Any) -> Callable[[], Any]: ...


FILTERING_OPTIONS_SEPARATOR = "__"


class FilteringOptions:
    """Looks for the filtering option"""

    def __init__(self):
        self.filter_options: Dict[str, FilterOptionProtocol] = {
            "eq": self._eq,
            "gt": self._gt,
            "gte": self._gte,
            "lt": self._lt,
            "lte": self._lte,
            "not": self._not,
            "is": self._is,
            "like": self._like,
            "regex": self._regex,
        }

    def get_default_filter(self) -> FilterOptionProtocol:
        return self._eq

    def parse_field(self, raw_field: str, value: Any) -> Callable:
        fields = raw_field.split(FILTERING_OPTIONS_SEPARATOR)
        last_field = fields[-1]

        if len(fields) == 1:
            filter_func = self.filter_options.get(last_field, self.get_default_filter())
            return filter_func(last_field, value)

        # Foreign Key

        if self.filter_options.get(fields[-1]) is None:
            foreign_field = raw_field
            filter_func = self.get_default_filter()
        else:
            foreign_field = FILTERING_OPTIONS_SEPARATOR.join(fields[:-1])
            filter_func = self.filter_options[fields[-1]]

        return filter_func(foreign_field, value)

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
        raise NotImplementedError(
            "_regex() is not implemented in the filtering options"
        )


__all__ = [
    "FilteringOptions",
    "FilterOptionProtocol",
    "FILTERING_OPTIONS_SEPARATOR",
]
