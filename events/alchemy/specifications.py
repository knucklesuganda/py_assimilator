from database.alchemy.specifications import FilterSpecification


class EventNotAckSpecification(FilterSpecification):
    def __init__(self, acknowledged_field: str):
        super(EventNotAckSpecification, self).__init__(**{acknowledged_field: False})
