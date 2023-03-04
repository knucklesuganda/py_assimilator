from typing import Callable, Union, List, Generator, Any

from assimilator.core.database.models import BaseModel
from assimilator.core.database.specifications import FilterSpecification
from assimilator.internal.database.specifications.filtering_options import InternalFilteringOptions


QueryT = Union[str, List[BaseModel]]


class InternalFilter(FilterSpecification):
    filtering_options_cls = InternalFilteringOptions

    def __init__(self, *filters, **named_filters):
        self.text_filters = [filter_ for filter_ in filters if isinstance(filter_, str)]

        if named_filters.get('id'):
            self.text_filters.append(named_filters.pop('id'))

        super(InternalFilter, self).__init__(
            *(set(filters) - set(self.text_filters)),
            **named_filters,
        )

    def apply(self, query: QueryT, **context) -> Union[str, Generator[BaseModel, Any, None]]:
        if isinstance(query, str):
            return f'{query}{"".join(self.text_filters)}'
        elif not self.filters:
            return query

        return (
            model for model in query
            if all(filter_func(model) for filter_func in self.filters)
        )

    def __or__(self, other: 'InternalFilter') -> 'InternalFilter':
        return OrInternalFilter(first_spec=self, second_spec=other)

    def __and__(self, other: 'InternalFilter') -> 'InternalFilter':
        specification = InternalFilter(*self.filters, *other.filters)
        specification.text_filters = self.text_filters + other.text_filters
        return specification

    @staticmethod
    def __inversion_func(func: Callable):
        def __inversion_func_wrapper(field, value):
            return not func(field, value)
        return __inversion_func_wrapper

    def __invert__(self):
        return InternalFilter(*map(
            lambda func, field, value: (self.__inversion_func(func), field, value),
            self.filters,
        ))


class OrInternalFilter(InternalFilter):
    def __init__(self, first_spec: InternalFilter, second_spec: InternalFilter):
        super(OrInternalFilter, self).__init__()
        self.first_spec = first_spec
        self.second_spec = second_spec

    def apply(self, query: QueryT, **context) -> Union[str, QueryT]:
        if isinstance(query, str):
            return f'{query}{"".join(self.first_spec.text_filters + self.second_spec.text_filters)}'

        first_filter = self.first_spec.apply(query)
        second_filter = self.second_spec.apply(query)
        return list(set(first_filter) | set(second_filter))


__all__ = ['InternalFilter']
