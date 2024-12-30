import json
from typing import (
    AbstractSet,
    Any,
    Callable,
    Dict,
    Mapping,
    Optional,
    Type,
    TypeVar,
    Union,
)
from uuid import UUID, uuid4

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Extra, Field, ValidationError

from assimilator.core.exceptions import ParsingError

T = TypeVar("T", bound="BaseModel")
AbstractSetIntStr = AbstractSet[Union[int, str]]
MappingIntStrAny = Mapping[Union[int, str], Any]


class BaseModel(PydanticBaseModel):
    id: str = Field(allow_mutation=False)

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True

    def __hash__(self):
        return UUID(self.id).int

    @property
    def autogenerate_id(self) -> bool:
        return True

    def generate_id(self, **kwargs) -> str:
        return str(uuid4())

    def __init__(self, **kwargs):
        if self.autogenerate_id and kwargs.get("id") is None:
            kwargs["id"] = self.generate_id(**kwargs)

        super().__init__(**kwargs)

    @classmethod
    def loads(cls: Type["T"], data: str) -> "T":
        try:
            return cls(**json.loads(data))
        except (ValidationError, TypeError) as exc:
            raise ParsingError(exc)


__all__ = [
    "BaseModel",
]
