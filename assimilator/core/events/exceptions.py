

class EventError(Exception):
    pass


class EventProducingError(EventError):
    pass


__all__ = [
    'EventError',
    'EventProducingError',
]
