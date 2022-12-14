from sqlalchemy.orm import Query

from assimilator.core.database.specifications import Specification, specification


class AlchemySpecification(Specification):
    def apply(self, query: Query) -> Query:
        return super(AlchemySpecification, self).apply(query)


@specification
def alchemy_filter(query: Query, *filters, **filters_by):
    return query.filter(*filters).filter_by(**filters_by)
