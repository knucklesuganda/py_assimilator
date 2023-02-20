from typing import ClassVar

from bson import ObjectId

from assimilator.core.database.models import BaseModel


class MongoModel(BaseModel):
    id: ObjectId
    upsert: bool = False

    class AssimilatorConfig(BaseModel.AssimilatorConfig):
        collection: ClassVar[str]

    class Config:
        exclude = (
            'collection',
            'upsert',
        )

    def __init__(self, **kwargs):
        super(MongoModel, self).__init__(**kwargs)

        if getattr(self.AssimilatorConfig, 'collection', None) is None:
            self.AssimilatorConfig.collection = self.__class__.__name__.lower()

    def generate_id(self, *args, **kwargs) -> ObjectId:
        return ObjectId()


__all__ = ['MongoModel']
