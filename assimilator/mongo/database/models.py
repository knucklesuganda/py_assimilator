from typing import ClassVar

from bson import ObjectId
from pydantic import Field

from assimilator.core.database.models import BaseModel


class MongoModel(BaseModel):
    upsert: bool = False
    id: ObjectId = Field(allow_mutation=False)

    class AssimilatorConfig:
        collection: ClassVar[str]
        autogenerate_id: ClassVar[bool] = True
        exclude = {'collection', 'upsert'}

    def __hash__(self):
        return int(str(self.id), base=16)

    def generate_id(self, **kwargs) -> ObjectId:
        return ObjectId()


__all__ = ['MongoModel']
