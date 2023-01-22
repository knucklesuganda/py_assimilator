import json
from uuid import uuid4
from typing import Type, Set

from pydantic import ValidationError, BaseModel as PydanticBaseModel

from assimilator.core.exceptions import ParsingError


class BaseModel(PydanticBaseModel):
    id: str

    class AssimilatorConfig:
        excluded_dumps: Set[str] = ()  # fields to exclude from dumps()
        autogenerate_id = True

    class Config:
        arbitrary_types_allowed = True

    def generate_id(self, *args, **kwargs) -> str:
        return str(uuid4())

    def __init__(self, **kwargs):
        if getattr(self.AssimilatorConfig, 'autogenerate_id', True) and (kwargs.get('id') is None):
            kwargs['id'] = self.generate_id(**kwargs)

        super(BaseModel, self).__init__(**kwargs)

    @classmethod
    def loads(cls: Type['BaseModel'], data: str) -> 'BaseModel':
        try:
            return cls(**json.loads(data))
        except ValidationError as exc:
            raise ParsingError(exc)

    def dumps(self, *args, **kwargs):
        if kwargs.get('exclude'):
            kwargs['exclude'] = set(*kwargs['exclude'], *getattr(self.AssimilatorConfig, 'excluded_dumps', ()))
        return super(BaseModel, self).json(*args, **kwargs)

    def dict(self, *args, **kwargs):
        if kwargs.get('exclude'):
            kwargs['exclude'] = set(*kwargs['exclude'], *getattr(self.AssimilatorConfig, 'excluded_dumps', ()))
        return super(BaseModel, self).dict(*args, **kwargs)


__all__ = [
    'BaseModel',
]
