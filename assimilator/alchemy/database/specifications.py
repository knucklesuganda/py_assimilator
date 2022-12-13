from sqlalchemy.orm import Query

from assimilator.core.database.specifications import Specification


class AlchemySpecification(Specification):
    def apply(self, query: Query) -> Query:
        return super(AlchemySpecification, self).apply(query)


class AlchemyFilterSpecification(AlchemySpecification):
    def __init__(self, *filters, **filters_by):
        self.filters = filters
        self.filters_by = filters_by

    def apply(self, query):
        return query.filter(*self.filters).filter_by(**self.filters_by)
