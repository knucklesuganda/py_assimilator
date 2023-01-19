from typing import TypeVar
from uuid import uuid4

from pydantic import BaseModel

from assimilator.core.patterns.mixins import JSONParsedMixin


T = TypeVar("T")
ComparableT = TypeVar("ComparableT")


class InternalModel(JSONParsedMixin, BaseModel):
    id: T

    class Meta:
        autogenerate_id = True

    def generate_id(self, *args, **kwargs) -> T:
        return str(uuid4())

    def __init__(self, *args, **kwargs):
        if self.Meta.autogenerate_id and (kwargs.get('id') is None):
            kwargs['id'] = self.generate_id(*args, **kwargs)

        super(InternalModel, self).__init__(*args, **kwargs)


__all__ = ['InternalModel']
