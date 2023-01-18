from typing import Optional

from assimilator.internal.database.models import InternalModel


class RedisModel(InternalModel):
    expire_in: Optional[int] = None
    expire_in_px: Optional[int] = None
    only_update: Optional[bool] = False   # Same as xx in redis set. Only set if key exists
    only_create: Optional[bool] = False   # Same as nx in redis set. Only set if key does not exist
    keep_ttl: Optional[bool] = False


__all__ = [
    'RedisModel',
]
