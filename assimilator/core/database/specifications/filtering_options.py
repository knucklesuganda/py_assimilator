from abc import abstractmethod
from typing import Dict, Tuple, Protocol, Any


class FilterOptionProtocol(Protocol):
    def __call__(self, field: str, value: Any):
        ...


class FilteringOptions:
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

    def parse_field(self, raw_field: str) -> Tuple[str, FilterOptionProtocol]:
        options = raw_field.split("__")

        if len(options) == 1:
            return options[0], self.filter_options.get(options[-1], self.get_default_filter())
        else:   # foreign key
            option = self.filter_options.get(options[-1])

            if option is None:
                field = ".".join(options)
                option = self.get_default_filter()
            else:
                field = ".".join(options[:-1])

            return field, option

    @abstractmethod
    def _eq(self, field: str, value):
        raise NotImplementedError("_eq() is not implemented in the filtering options")

    @abstractmethod
    def _gt(self, field: str, value):
        raise NotImplementedError("_gt() is not implemented in the filtering options")

    @abstractmethod
    def _gte(self, field: str, value):
        raise NotImplementedError("_gte() is not implemented in the filtering options")

    @abstractmethod
    def _lt(self, field: str, value):
        raise NotImplementedError("_lt() is not implemented in the filtering options")

    @abstractmethod
    def _lte(self, field: str, value):
        raise NotImplementedError("_lte() is not implemented in the filtering options")

    @abstractmethod
    def _not(self, field: str, value):
        raise NotImplementedError("_not() is not implemented in the filtering options")

    @abstractmethod
    def _is(self, field: str, value):
        raise NotImplementedError("_is() is not implemented in the filtering options")

    @abstractmethod
    def _like(self, field: str, value):
        raise NotImplementedError("_like() is not implemented in the filtering options")

    @abstractmethod
    def _regex(self, field: str, value):
        raise NotImplementedError("_regex() is not implemented in the filtering options")


__all__ = [
    'FilteringOptions',
    'FilterOptionProtocol',
]
