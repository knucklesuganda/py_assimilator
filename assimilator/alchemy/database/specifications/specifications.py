from itertools import zip_longest
from typing import Collection, Optional, Iterable, Any, Dict, Callable

from sqlalchemy.orm import load_only, Load
from sqlalchemy import column, desc, and_, or_, not_, Select, inspect

from assimilator.alchemy.database.model_utils import get_model_from_relationship
from assimilator.alchemy.database.specifications.filtering_options import AlchemyFilteringOptions
from assimilator.core.database.specifications import (
    specification,
    SpecificationList,
    SpecificationType,
    FilterSpecification,
)


class AlchemyFilter(FilterSpecification):
    filtering_options_cls = AlchemyFilteringOptions

    def __init__(self, *filters, **named_filters):
        super(AlchemyFilter, self).__init__(*filters)
        self._named_filters = named_filters
        self._filters_parsed: bool = False

    def __or__(self, other: 'AlchemyFilter') -> SpecificationType:
        return AlchemyChainSpecification(self, other, or_)

    def __and__(self, other: 'AlchemyFilter') -> SpecificationType:
        return AlchemyChainSpecification(self, other, and_)

    def __invert__(self):
        return AlchemyFilter(not_(*self.filters))

    def parse_filters(self, model):
        if self._filters_parsed:
            return

        self.filtering_options.table_name = str(inspect(model).selectable)
        for field, value in self._named_filters.items():
            self.filters.append(self.filtering_options.parse_field(raw_field=field, value=value))

        self._filters_parsed = True

    def apply(self, query: Select, **context: Any) -> Select:
        self.parse_filters(context['repository'].model)
        return query.filter(*self.filters)


class AlchemyChainSpecification(AlchemyFilter):
    def __init__(self, first: AlchemyFilter, second: AlchemyFilter, func: Callable):
        super(AlchemyChainSpecification, self).__init__()
        self.first = first
        self.second = second
        self.func = func

    def apply(self, query: Select, **context: Any) -> Select:
        self.first.parse_filters(context['repository'].model)
        self.second.parse_filters(context['repository'].model)
        return query.filter(self.func(*self.first.filters, *self.second.filters))


alchemy_filter = AlchemyFilter


@specification
def alchemy_order(*clauses: str, query: Select, **_) -> Select:
    parsed_clauses = []

    for clause in clauses:
        if clause.startswith("-"):
            parsed_clauses.append(desc(column(clause[1:])))
        else:
            parsed_clauses.append(clause)

    return query.order_by(*parsed_clauses)


@specification
def alchemy_paginate(
    *,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    query: Select,
    **_,
) -> Select:
    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)

    return query


@specification
def alchemy_join(
    *targets: Collection,
    join_args: Iterable[dict] = None,
    query: Select,
    model,
    **_,
) -> Select:
    for target, join_data in zip_longest(targets, (join_args or {}), fillvalue=dict()):
        if not target:
            continue

        if isinstance(target, str):
            entities = target.split(".")
            target = model

            for entity in entities:
                target, _ = get_model_from_relationship(
                    model=target,
                    relationship_name=entity,
                )

        query = query.join(target, **join_data).add_columns(target).select_from(model)

    return query


@specification
def alchemy_only(
    *only_fields: str,
    query: Select,
    model,
    **_,
):
    models_to_fields: Dict[Load, Any] = {}
    parsed_loads = list(field for field in only_fields if not isinstance(field, str))

    if parsed_loads:
        query = query.options(load_only(*parsed_loads))

    for field in (field for field in only_fields if isinstance(field, str)):
        parts = field.split('.')
        if len(parts) == 1:
            models_to_fields[Load(model)] = [
                getattr(model, field),
                *models_to_fields.get(model, []),
            ]
            continue

        current_load = model
        for part in parts:
            model_relationships = set(inspect(current_load).relationships.keys())

            if part in model_relationships:
                current_load, _ = get_model_from_relationship(current_load, relationship_name=part)
            else:
                models_to_fields[Load(current_load)] = [
                    getattr(current_load, part),
                    *models_to_fields.get(current_load, []),
                ]
                break

        else:
            models_to_fields[Load(current_load)] = []

    for loader, load_fields in models_to_fields.items():
        if load_fields:
            query = query.options(loader.load_only(*load_fields))
        else:
            query = query.options(loader)

    return query


class AlchemySpecificationList(SpecificationList):
    filter = AlchemyFilter
    order = alchemy_order
    paginate = alchemy_paginate
    join = alchemy_join
    only = alchemy_only


__all__ = [
    'AlchemySpecificationList',
    'alchemy_filter',
    'AlchemyFilter',
    'alchemy_order',
    'alchemy_paginate',
    'alchemy_join',
    'alchemy_only',
]
