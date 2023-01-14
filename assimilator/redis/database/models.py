from typing import Optional

from assimilator.internal.database.models import InternalModel


class RedisModel(InternalModel):
    expire_in: Optional[int] = None


__all__ = [
    'RedisModel',
]
