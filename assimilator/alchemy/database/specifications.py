from sqlalchemy import not_, or_, and_
from sqlalchemy.orm import Query

from assimilator.core.database.specification import Specification, OrSpecification, AndSpecification, NotSpecification


class AlchemyNotSpecification(NotSpecification):
    def apply(self, query):
        return not_(self.specification(query))


class AlchemyAndSpecification(AndSpecification):
    def apply(self, query):
        return and_(self.first(query), self.second(query))


class AlchemyOrSpecification(OrSpecification):
    def apply(self, query):
        return or_(self.first(query), self.second(query))


class AlchemySpecification(Specification):
    and_specification = AlchemyAndSpecification
    or_specification = AlchemyOrSpecification
    not_specification = AlchemyNotSpecification

    def apply(self, query: Query) -> Query:
        return super(AlchemySpecification, self).apply(query)


class FilterSpecification(AlchemySpecification):
    def __init__(self, *filters, **filters_by):
        self.filters = filters
        self.filters_by = filters_by

    def apply(self, query):
        return query.filter(*self.filters).filter_by(**self.filters_by)


class ValueInSpecification(AlchemySpecification):
    def __init__(self, field, values):
        super(ValueInSpecification, self).__init__(field.in_(values))
