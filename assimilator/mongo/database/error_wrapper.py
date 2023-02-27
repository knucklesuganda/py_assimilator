from bson.errors import BSONError
from pymongo.errors import DuplicateKeyError, InvalidOperation, WriteError

from assimilator.core.patterns import ErrorWrapper
from assimilator.core.exceptions import ParsingError
from assimilator.core.database import DataLayerError, InvalidQueryError, NotFoundError


class MongoErrorWrapper(ErrorWrapper):
    def __init__(self):
        super(MongoErrorWrapper, self).__init__(
            error_mappings={
                BSONError: ParsingError,
                DuplicateKeyError: InvalidQueryError,
                InvalidOperation: InvalidQueryError,
                WriteError: InvalidQueryError,
            },
            skipped_errors={NotFoundError},
            default_error=DataLayerError,
        )


__all__ = ['MongoErrorWrapper']
