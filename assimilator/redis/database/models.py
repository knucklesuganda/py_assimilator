from typing import Any

from pydantic import BaseModel

from assimilator.core.patterns.mixins import JSONParsedMixin


class RedisModel(JSONParsedMixin, BaseModel):
    id: int
    value: Any
