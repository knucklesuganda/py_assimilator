from operator import or_, and_
from typing import Union, List, Generator, Any

from assimilator.core.database.models import BaseModel
from assimilator.core.database import FilterSpecification
from assimilator.internal.database.specifications.internal_operator import invert
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

    def __call__(self, query: QueryT, **context) -> Union[str, Generator[BaseModel, Any, None]]:
        if isinstance(query, str):
            return f'{query}{"".join(str(filter_) for filter_ in self.text_filters)}'
        elif not self.filters:
            return query

        return (
            model for model in query
            if all(filter_func(model) for filter_func in self.filters)
        )

    def __or__(self, other: Union['InternalFilter', 'CompositeFilter']) -> 'InternalFilter':
        return CompositeFilter(first=self, second=other, operation=or_)

    def __and__(self, other: Union['InternalFilter', 'CompositeFilter']) -> 'InternalFilter':
        return CompositeFilter(first=self, second=other, operation=and_)

    def __invert__(self):
        return InternalFilter(*(invert(func) for func in self.filters))


class CompositeFilter(InternalFilter):
    def __init__(
        self,
        first: Union[FilterSpecification, 'CompositeFilter'],
        second: Union[FilterSpecification, 'CompositeFilter'],
        operation: Union[or_, and_],
    ):
        super(CompositeFilter, self).__init__()
        self.first = first
        self.second = second
        self.operation = operation

    def __call__(self, query: QueryT, **context) -> Union[str, QueryT]:
        if isinstance(query, str):
            first_result = self.first(query=query, **context)
            second_result = self.second(query=query, **context)
            return f'{query}{first_result.replace(query, "")}{second_result.replace(query, "")}'

        first_result = self.first(query=query, **context)
        second_result = self.second(query=query, **context)

        return list(self.operation(set(first_result), set(second_result)))

    def __str__(self):
        return f"{self.first} {self.operation} {self.second}"


__all__ = ['InternalFilter']
