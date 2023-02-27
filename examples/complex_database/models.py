from typing import List

from sqlalchemy import create_engine, Column, String, Float, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

from assimilator.core.database import BaseModel
from assimilator.mongo.database import MongoModel
from assimilator.redis_.database import RedisModel

engine = create_engine(url="sqlite:///:memory:")
Base = declarative_base()


class AlchemyUser(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    username = Column(String())
    email = Column(String())

    balances = relationship("AlchemyUserBalance", back_populates="user")

    def __str__(self):
        return f"{self.id} {self.username} {self.email}"


class AlchemyUserBalance(Base):
    __tablename__ = "balances"
    __table_args__ = (
        UniqueConstraint("balance", "user_id"),
    )

    id = Column(Integer(), primary_key=True)

    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("AlchemyUser", back_populates="balances")

    balance = Column(Float(), server_default='0')

    currency_id = Column(ForeignKey("currency.id"))
    currency = relationship("AlchemyBalanceCurrency", uselist=False)

    def __str__(self):
        return f"{self.balance}{self.currency.currency}"

    def __repr__(self):
        return str(self)


class AlchemyBalanceCurrency(Base):
    __tablename__ = "currency"

    id = Column(Integer(), primary_key=True)
    currency = Column(String(length=20))
    country = Column(String(length=20))

    def __str__(self):
        return self.currency

    def __repr__(self):
        return str(self)


Base.metadata.create_all(engine)


class InternalCurrency(BaseModel):
    currency: str
    country: str


class InternalBalance(BaseModel):
    balance: float
    currency: InternalCurrency


class InternalUser(BaseModel):
    username: str
    email: str
    balances: List[InternalBalance] = []


class RedisCurrency(InternalCurrency):
    pass


class RedisBalance(InternalBalance, RedisModel):
    currency: RedisCurrency


class RedisUser(InternalUser, RedisModel):
    balances: List[RedisBalance] = []


class MongoCurrency(MongoModel):
    class AssimilatorConfig:
        collection: str = "currencies"
        autogenerate_id = True

    currency: str
    country: str


class MongoBalance(MongoModel):
    class AssimilatorConfig:
        collection: str = "balances"

    balance: float
    currency: MongoCurrency


class MongoUser(MongoModel):
    class AssimilatorConfig:
        collection: str = "users"

    balances: List[MongoBalance] = []
    username: str
    email: str
