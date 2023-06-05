from typing import ClassVar, Any, Union, AbstractSet, Mapping, Dict

from bson import ObjectId
from pydantic import Field

from assimilator.core.database.models import BaseModel

AbstractSetIntStr = AbstractSet[Union[int, str]]
MappingIntStrAny = Mapping[Union[int, str], Any]


class MongoModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
        json_encoders = {
            ObjectId: str,
        }

    class AssimilatorConfig:
        collection: ClassVar[str]
        autogenerate_id: ClassVar[bool] = True
        exclude = {'collection': True, 'upsert': True}
        id_name: ClassVar[str] = "_id"

    upsert: bool = False
    id: ObjectId = Field(alias="_id")

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__fields__['id'].alias = cls.AssimilatorConfig.id_name
        return cls

    def __hash__(self):
        return int(str(self.id), base=16)

    def generate_id(self, **kwargs) -> ObjectId:
        return ObjectId()

    def json(self, *args, by_alias: bool = True, **kwargs) -> str:
        return super(BaseModel, self).json(*args, by_alias=by_alias, **kwargs)

    def dict(self, *args, by_alias: bool = True, **kwargs) -> Dict[str, Any]:
        return super(BaseModel, self).dict(*args, by_alias=by_alias, **kwargs)


__all__ = ['MongoModel']
