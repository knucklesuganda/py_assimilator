

class DataLayerError(Exception):
    """ Any error related to Repository, UnitOfWork, Model """


class NotFoundError(DataLayerError):
    """ Results are not found """


class InvalidQueryError(DataLayerError):
    """ The query to the data storage supplied was invalid """


class MultipleResultsError(InvalidQueryError):
    """ Repository get() function returned more than one result """
