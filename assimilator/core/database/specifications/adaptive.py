from typing import Optional, Iterable

from assimilator.core.database import Repository, specification


class Filter:
    def __init__(self, *fields, **kwargs_fields):
        self.fields = fields
        self.kwargs_fields = kwargs_fields

    def __call__(self, query, repository: Repository, **context):
        return repository.specs.filter(
            *self.fields, **self.kwargs_fields)(query=query, repository=repository)


filter_ = Filter


@specification
def order(*clauses: str, query, repository: Repository, **context):
    return repository.specs.order(*clauses)(query=query, repository=repository, **context)


@specification
def paginate(*, limit: Optional[int] = None, offset: Optional[int] = None, query, repository: Repository, **context):
    return repository.specs.paginate(limit=limit, offset=offset)(query=query, repository=repository, **context)


@specification
def join(*targets: str, join_args: Iterable[dict] = None, query, repository: Repository, **context):
    return repository.specs.join(*targets, join_args=join_args)(query=query, repository=repository, **context)


@specification
def only(*only_fields: str, query, repository: Repository, **context):
    return repository.specs.only(*only_fields)(query=query, repository=repository, **context)


__all__ = [
    'Filter',
    'filter_',
    'only',
    'order',
    'join',
    'paginate',
]
