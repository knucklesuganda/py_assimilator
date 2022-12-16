from database.base.specification import Specification


class FilterSpecification(Specification):
    def __init__(self, *filters, **filters_by):
        self.filters = filters
        self.filters_by = filters_by

    def apply(self, query):
        return query.filter(*self.filters).filter_by(**self.filters_by)