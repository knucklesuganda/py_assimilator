from typing import Callable, Any, Optional, Collection

from assimilator.mongo.database.specifications import MongoFilteringOptions
from assimilator.core.database import SpecificationList, FilterSpecification, specification


class MongoFilterSpecification(FilterSpecification):
    filters: dict
    filtering_options_cls = MongoFilteringOptions

    def __init__(self, *filters, **named_filters):
        super(MongoFilterSpecification, self).__init__(*filters, **named_filters)
        parsed_filters = {}

        for filter_ in self.filters:
            parsed_filters.update(filter_)

        self.filters = parsed_filters

    def get_parsed_filter(self, filter_func: Callable, field: str, value: Any) -> dict:
        return filter_func(field, value)

    def __or__(self, other: 'FilterSpecification') -> 'FilterSpecification':
        return MongoFilterSpecification({"$or": [self.filters, other.filters]})

    def __and__(self, other: 'FilterSpecification') -> 'FilterSpecification':
        return MongoFilterSpecification({**self.filters, **other.filters})

    def __invert__(self) -> 'MongoFilterSpecification':
        inverted_filters = []

        for column, value in self.filters.items():
            inverted_filters.append({column: {"$not": value}})

        return MongoFilterSpecification(*inverted_filters)

    def apply(self, query: dict) -> dict:
        query['filter'] = {**query.get('filter', {}), **self.filters}
        return query


@specification
def mongo_order(*clauses: str, query: dict) -> dict:
    query['sort'] = {
        **query.get('sort', {}),
        **{column: -1 if column.startswith("-") else 1 for column in clauses}
    }
    return query


@specification
def mongo_paginate(*, limit: Optional[int] = None, offset: Optional[int] = None, query: dict) -> dict:
    if offset is not None:
        query['skip'] = offset
    if limit is not None:
        query['limit'] = limit

    return query


@specification
def mongo_join(*targets: Collection, query: dict, **join_args: dict) -> dict:
    return query    # TODO: finish join


@specification
def mongo_only(*only_fields: str, query: dict) -> dict:
    query['projection'] = only_fields
    return query


class MongoSpecificationList(SpecificationList):
    filter = MongoFilterSpecification
    order = mongo_order
    paginate = mongo_paginate
    join = mongo_join
    only = mongo_only


__all__ = [
    'MongoSpecificationList',
    'MongoFilterSpecification',
    'mongo_order',
    'mongo_paginate',
    'mongo_join',
    'mongo_only',
]
