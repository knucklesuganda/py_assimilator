from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import declarative_base

from core.database import BaseModel
from mongo.database import MongoModel
from redis_.database import RedisModel

engine = create_engine(url="sqlite:///:memory:")
Base = declarative_base()


class AlchemyUser(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    username = Column(String())
    email = Column(String())
    balance = Column(Float())

    def __str__(self):
        return f"{self.id} {self.username} {self.email}"


Base.metadata.create_all(engine)


class InternalUser(BaseModel):
    username: str
    email: str
    balance: float


class RedisUser(RedisModel):
    username: str
    email: str
    balance: float


class MongoUser(MongoModel):

    @staticmethod
    def get_collection():
        return "users"
