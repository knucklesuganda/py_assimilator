import json
from typing import Type

from pydantic import ValidationError, BaseModel

from assimilator.core.exceptions import ParsingError


class JSONParsedMixin:
    @classmethod
    def from_json(cls: Type['BaseModel'], data: str) -> 'BaseModel':
        try:
            return cls(**json.loads(data))
        except ValidationError as exc:
            raise ParsingError(exc)


__all__ = [
    'JSONParsedMixin',
]
