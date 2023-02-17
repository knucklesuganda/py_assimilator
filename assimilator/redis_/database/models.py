from typing import Optional

from assimilator.core.database.models import BaseModel


class RedisModel(BaseModel):
    expire_in: Optional[int] = None
    expire_in_px: Optional[int] = None
    only_update: Optional[bool] = False   # Same as xx in redis set. Only set if key exists
    only_create: Optional[bool] = False   # Same as nx in redis set. Only set if key does not exist
    keep_ttl: Optional[bool] = False

    class Config(BaseModel.Config):
        exclude = (
            'expire_in',
            'expire_in_px',
            'only_update',
            'only_create',
            'keep_ttl',
        )


__all__ = [
    'RedisModel',
]
