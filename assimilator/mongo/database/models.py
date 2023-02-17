from bson import ObjectId
from pydantic import Extra

from assimilator.core.database.models import BaseModel


class MongoModel(BaseModel):
    id: ObjectId
    upsert: bool = False

    class Config(BaseModel.Config):
        exclude = (
            'collection',
            'upsert',
        )
        collection: str
        extra = Extra.allow

    def __init__(self, **kwargs):
        super(MongoModel, self).__init__(**kwargs)

        if getattr(self.Config, 'collection', None) is None:
            self.Config.collection = self.__class__.__name__.lower()

    def generate_id(self, *args, **kwargs) -> ObjectId:
        return ObjectId()


__all__ = ['MongoModel']
