from assimilator.core.exceptions import ParsingError


class EventError(Exception):
    pass


class EventParsingError(ParsingError, EventError):
    pass


class EventProducingError(EventError):
    pass


__all__ = [
    'EventError',
    'EventParsingError',
    'EventProducingError',
]
