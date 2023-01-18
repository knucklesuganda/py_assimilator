from assimilator.core.database.exceptions import DataLayerError, NotFoundError
from assimilator.core.patterns.error_wrapper import ErrorWrapper


class InternalErrorWrapper(ErrorWrapper):
    def __init__(self):
        super(InternalErrorWrapper, self).__init__(error_mappings={
            KeyError: NotFoundError,
            TypeError: NotFoundError,
        }, default_error=DataLayerError)


__all__ = ['InternalErrorWrapper']
