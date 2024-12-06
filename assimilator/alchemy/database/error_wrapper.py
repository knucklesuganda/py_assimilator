from sqlalchemy.exc import (
    IntegrityError,
    MultipleResultsFound,
    NoResultFound,
    SQLAlchemyError,
)

from assimilator.core.database.exceptions import (
    DataLayerError,
    InvalidQueryError,
    MultipleResultsError,
    NotFoundError,
)
from assimilator.core.patterns.error_wrapper import ErrorWrapper


class AlchemyErrorWrapper(ErrorWrapper):
    def __init__(self):
        super(AlchemyErrorWrapper, self).__init__(
            error_mappings={
                NoResultFound: NotFoundError,
                IntegrityError: InvalidQueryError,
                SQLAlchemyError: DataLayerError,
                MultipleResultsFound: MultipleResultsError,
            },
            default_error=DataLayerError,
        )


__all__ = ["AlchemyErrorWrapper"]
