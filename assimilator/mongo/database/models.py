from typing import AbstractSet, Any, Mapping, Union

from bson import ObjectId
from pydantic import Field

from assimilator.core.database.models import BaseModel

AbstractSetIntStr = AbstractSet[Union[int, str]]
MappingIntStrAny = Mapping[Union[int, str], Any]


class MongoModel(BaseModel):
    class Config:
        populate_by_name = True
        use_enum_values = True
        json_encoders = {ObjectId: str}

    @property
    def collection(self) -> str:
        return ""

    @property
    def id_name(self) -> str:
        return "_id"

    upsert: bool = False
    id: ObjectId = Field(alias="_id")

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__fields__["id"].alias = cls.id_name
        return cls

    def __hash__(self):
        return int(str(self.id), base=16)

    def generate_id(self, **kwargs) -> ObjectId:
        return ObjectId()


__all__ = ["MongoModel"]
