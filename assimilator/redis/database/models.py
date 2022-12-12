from pydantic import BaseModel


class RedisModel(BaseModel):
    id: int
