from typing import Optional

from pydantic import BaseModel

from assimilator.core.patterns.mixins import JSONParsedMixin


class RedisModel(JSONParsedMixin, BaseModel):
    id: int
    expire_in: Optional[int] = None
