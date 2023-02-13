from typing import Callable, Any, Union, List, Set, Dict, Tuple

from assimilator.core.database.specifications import FilterSpecification
from assimilator.internal.database.specifications.filtering_options import InternalFilteringOptions
from assimilator.core.database.models import BaseModel


QueryT = Union[str, List[BaseModel]]
Containers = (List, Set, Tuple)


class InternalFilter(FilterSpecification):
    filtering_options_cls = InternalFilteringOptions

    def __init__(self, *filters, **named_filters):
        self.text_filters = [filter_ for filter_ in filters if isinstance(filter_, str)]

        if named_filters.get('id'):
            self.text_filters.append(named_filters.pop('id'))

        super(InternalFilter, self).__init__(*(set(filters) - set(self.text_filters)), **named_filters)

    def get_parsed_filter(self, filter_func: Callable, field: str, value: Any):
        return filter_func, field, value

    def _get_model_field(self, model, field: str):
        foreign_fields = field.split(".")

        field_val = model
        for foreign_field in foreign_fields:
            if isinstance(field_val, Containers):
                field_val = list(map(lambda obj: getattr(obj, foreign_field), field_val))
            elif isinstance(field_val, Dict):   # TODO: what to do with different data types???
                field_val = list(map(lambda obj: getattr(obj, foreign_field), field_val.values()))
            else:
                field_val = getattr(field_val, foreign_field)

        return field_val

    def _check_model_passes(self, model) -> bool:

        for filter_func, field, value in self.filters:
            field_value = self._get_model_field(model, field)

            if isinstance(field_value, list) and not isinstance(value, list):
                if not any(filter_func(attr, value) for attr in field_value):
                    return False
            elif not filter_func(field_value, value):
                return False

        return True

    def apply(self, query: QueryT) -> Union[str, QueryT]:
        if isinstance(query, str):
            return f'{query}{"".join(self.text_filters)}'
        elif not self.filters:
            return query

        return list(filter(lambda model: self._check_model_passes(model), query))

    def __or__(self, other: 'InternalFilter') -> 'InternalFilter':
        return OrInternalFilter(first_spec=self, second_spec=other)

    def __and__(self, other: 'InternalFilter') -> 'InternalFilter':
        specification = InternalFilter(*self.filters, other.filters)
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
        self.text_filters = first_spec.text_filters + second_spec.text_filters
        self.first_spec = first_spec
        self.second_spec = second_spec

    def apply(self, query: QueryT) -> Union[str, QueryT]:
        if isinstance(query, str):
            return f'{query}{"".join(self.text_filters)}'

        first_filter = self.first_spec.apply(query)
        second_filter = self.second_spec.apply(query)
        return list(set(first_filter) | set(second_filter))


__all__ = ['InternalFilter']
