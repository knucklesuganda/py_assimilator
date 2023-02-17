import json
from uuid import uuid4
from typing import Type, Set, TypeVar

from pydantic import ValidationError, BaseModel as PydanticBaseModel

from assimilator.core.exceptions import ParsingError


T = TypeVar("T", bound='BaseModel')


class BaseModel(PydanticBaseModel):
    id: str

    class Config:
        arbitrary_types_allowed = True
        autogenerate_id = True

    def generate_id(self, **kwargs) -> str:
        return str(uuid4())

    def __init__(self, **kwargs):
        if self.Config.autogenerate_id and kwargs.get('id') is None:
            kwargs['id'] = self.generate_id(**kwargs)

        super(BaseModel, self).__init__(**kwargs)

    @classmethod
    def loads(cls: Type['T'], data: str) -> 'T':
        try:
            return cls(**json.loads(data))
        except (ValidationError, TypeError) as exc:
            raise ParsingError(exc)


__all__ = [
    'BaseModel',
]
