from typing import ClassVar

from bson import ObjectId

from assimilator.core.database.models import BaseModel


class MongoModel(BaseModel):
    upsert: bool = False
    id: ObjectId

    class AssimilatorConfig(BaseModel.AssimilatorConfig):
        collection: ClassVar[str]
        autogenerate_id: ClassVar[bool] = True

    class Config:
        exclude = {
            'collection': True,
            'upsert': True,
        }
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        super(MongoModel, self).__init__(**kwargs)

    def generate_id(self, **kwargs) -> ObjectId:
        return ObjectId()


__all__ = ['MongoModel']
