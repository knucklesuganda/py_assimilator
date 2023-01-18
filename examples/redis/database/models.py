from assimilator.redis_.database import RedisModel


class RedisUser(RedisModel):
    username: str
    email: str
    balance: float = 0


__all__ = ['RedisUser']
