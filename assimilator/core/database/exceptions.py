

class DataLayerError(Exception):
    pass


class NotFoundError(DataLayerError):
    pass


class InvalidQueryError(DataLayerError):
    pass


class ParsingError(DataLayerError):
    pass
