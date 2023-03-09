import operator
from typing import Optional, Iterable, Union, Callable, Tuple

from assimilator.core.database.specifications.specifications import specification, FilterSpecification


class Filter:
    def __init__(self, *fields, **kwargs_fields):
        self.fields = fields
        self.kwargs_fields = kwargs_fields

    def _get_specification(self, repository, *fields, **kwargs_fields) -> 'FilterSpecification':
        return repository.specs.filter(*fields, **kwargs_fields)

    def __or__(self, other: Union['Filter', 'FilterSpecification']) -> 'CompositeFilter':
        return CompositeFilter(first=self, second=other, func=operator.or_)

    def __and__(self, other: Union['Filter', 'FilterSpecification']) -> 'CompositeFilter':
        return CompositeFilter(first=self, second=other, func=operator.and_)

    def __invert__(self):
        return Filter(self.fields, self.kwargs_fields)

    def __call__(self, query, repository, **context):
        return self._get_specification(
            repository,
            *self.fields,
            **self.kwargs_fields,
        )(query=query, repository=repository)


class CompositeFilter(Filter):
    def __init__(
        self,
        first: Union['Filter', 'FilterSpecification'],
        second: Union['Filter', 'FilterSpecification'],
        func: Callable,
    ):
        super(CompositeFilter, self).__init__()
        self.first = first
        self.second = second
        self.func = func

    def _parse_specification(
        self, repository, spec: Union['Filter', 'FilterSpecification']
    ) -> Tuple[Union['FilterSpecification', 'CompositeFilter'], bool]:
        if isinstance(spec, Filter) and not isinstance(spec, CompositeFilter):
            return self._get_specification(
                repository=repository,
                *spec.fields,
                **spec.kwargs_fields,
            ), True

        return spec, False

    def __call__(self, query, repository, **context):
        first, first_is_simple = self._parse_specification(repository=repository, spec=self.first)
        second, _ = self._parse_specification(repository=repository, spec=self.second)

        return self.func(second, first)(query=query, repository=repository, **context)


filter_ = Filter


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
    'Filter',
    'filter_',
    'only',
    'order',
    'join',
    'paginate',
]
