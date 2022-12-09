from sqlalchemy.exc import IntegrityError


class NotFoundError(Exception):
    pass


class InvalidQueryError(IntegrityError):
    pass
