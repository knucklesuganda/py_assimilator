import operator
from typing import Optional, Iterable, Union, Callable, Any

from assimilator.core.database.specifications.specifications import specification, FilterSpecification


class AdaptiveFilter:
    def __init__(self, *fields, **kwargs_fields):
        self.fields = fields
        self.kwargs_fields = kwargs_fields

    def __or__(self, other: Union['AdaptiveFilter', 'FilterSpecification']) -> 'CompositeAdaptiveFilter':
        return CompositeAdaptiveFilter(first=self, second=other, func=operator.or_)

    def __and__(self, other: Union['AdaptiveFilter', 'FilterSpecification']) -> 'CompositeAdaptiveFilter':
        return CompositeAdaptiveFilter(first=self, second=other, func=operator.and_)

    def __invert__(self):
        return AdaptiveFilter(self.fields, self.kwargs_fields)

    def __call__(self, query, repository, **context):
        return repository.specs.filter(
            *self.fields, **self.kwargs_fields,
        )(query=query, repository=repository)


class CompositeAdaptiveFilter(AdaptiveFilter):
    def __init__(
        self,
        first: Union['AdaptiveFilter', 'FilterSpecification'],
        second: Union['AdaptiveFilter', 'FilterSpecification'],
        func: Callable[['AdaptiveFilter', 'AdaptiveFilter'], Any],
    ):
        super(CompositeAdaptiveFilter, self).__init__()
        self.first = first
        self.second = second
        self.func = func

    def _parse_specification(self, filter_spec, repository):
        if isinstance(filter_spec, CompositeAdaptiveFilter):
            first = self._parse_specification(filter_spec=filter_spec.first, repository=repository)
            second = self._parse_specification(filter_spec=filter_spec.second, repository=repository)
            return filter_spec.func(first, second)

        elif isinstance(filter_spec, AdaptiveFilter):
            return repository.specs.filter(*filter_spec.fields, **filter_spec.kwargs_fields)
        else:
            return filter_spec

    def __call__(self, query, repository, **context):
        first = self._parse_specification(filter_spec=self.first, repository=repository)
        second = self._parse_specification(filter_spec=self.first, repository=repository)
        return self.func(first, second)(query=query, repository=repository, **context)


filter_ = AdaptiveFilter


@specification
def order(*clauses: str, query, repository, **context):
    return repository.specs.order(*clauses)(query=query, repository=repository, **context)


@specification
def paginate(
    *,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    query,
    repository,
    **context,
):
    paginate_spec = repository.specs.paginate(limit=limit, offset=offset)
    return paginate_spec(query=query, repository=repository, **context)


@specification
def join(*targets: str, join_args: Iterable[dict] = None, query, repository, **context):
    return repository.specs.join(*targets, join_args=join_args)(query=query, repository=repository, **context)


@specification
def only(*only_fields: str, query, repository, **context):
    return repository.specs.only(*only_fields)(query=query, repository=repository, **context)


__all__ = [
    'AdaptiveFilter',
    'filter_',
    'only',
    'order',
    'join',
    'paginate',
]
