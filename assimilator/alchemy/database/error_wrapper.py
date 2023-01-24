from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError, MultipleResultsFound

from assimilator.core.database.exceptions import (
    DataLayerError,
    NotFoundError,
    InvalidQueryError,
    MultipleResultsError,
)
from assimilator.core.patterns.error_wrapper import ErrorWrapper


class AlchemyErrorWrapper(ErrorWrapper):
    def __init__(self):
        super(AlchemyErrorWrapper, self).__init__(error_mappings={
            NoResultFound: NotFoundError,
            IntegrityError: InvalidQueryError,
            SQLAlchemyError: DataLayerError,
            MultipleResultsFound: MultipleResultsError,
        }, default_error=DataLayerError)


__all__ = ['AlchemyErrorWrapper']
