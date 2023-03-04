from typing import ClassVar

from bson import ObjectId

from assimilator.core.database.models import BaseModel


class MongoModel(BaseModel):
    upsert: bool = False
    id: ObjectId

    class AssimilatorConfig:
        collection: ClassVar[str]
        autogenerate_id: ClassVar[bool] = True
        exclude = {'collection', 'upsert'}

    def generate_id(self, **kwargs) -> ObjectId:
        return ObjectId()


__all__ = ['MongoModel']
