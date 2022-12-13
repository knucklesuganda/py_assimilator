from assimilator.core.database.exceptions import ParsingError


class EventError(Exception):
    pass


class EventParsingError(ParsingError, EventError):
    pass


class EventProducingError(EventError):
    pass
