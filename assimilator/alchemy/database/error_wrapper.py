from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError

from assimilator.core.database.exceptions import DataLayerError, NotFoundError, InvalidQueryError
from assimilator.core.patterns.error_wrapper import ErrorWrapper


class AlchemyErrorWrapper(ErrorWrapper):
    def __init__(self):
        super(AlchemyErrorWrapper, self).__init__(error_mappings={
            NoResultFound: NotFoundError,
            IntegrityError: InvalidQueryError,
            SQLAlchemyError: DataLayerError,
        }, default_error=DataLayerError)


__all__ = ['AlchemyErrorWrapper']
