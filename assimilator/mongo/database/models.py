from bson import ObjectId
from pydantic import Extra

from assimilator.core.database.models import BaseModel


class MongoModel(BaseModel):
    id: ObjectId
    upsert: bool = False

    class AssimilatorConfig:
        excluded_dumps = (
            'collection',
            'upsert',
        )

    class Config:
        extra = Extra.allow

    @staticmethod
    def get_collection():
        raise NotImplementedError("collection() is not implemented for the model")

    @property
    def _id(self):
        return self.id

    def generate_id(self, *args, **kwargs) -> ObjectId:
        return ObjectId()


__all__ = ['MongoModel']
