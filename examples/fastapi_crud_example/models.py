from typing import List

from sqlalchemy import (
    create_engine, Column, String, Float,
    Integer, ForeignKey, UniqueConstraint, Table,
)
from sqlalchemy.orm import relationship, registry

from assimilator.core.database import BaseModel
from assimilator.mongo.database import MongoModel
from assimilator.redis_.database import RedisModel

engine = create_engine(url="sqlite:///:memory:")
mapper_registry = registry()

users = Table(
    "users",
    mapper_registry.metadata,
    Column("id", Integer(), primary_key=True),
    Column("username", String()),
    Column("email", String()),
)


balances = Table(
    "balances",
    mapper_registry.metadata,
    Column('id', Integer(), primary_key=True),
    Column('user_id', ForeignKey("users.id", ondelete="CASCADE")),
    Column('balance', Float(), server_default='0'),
    Column('currency_id', ForeignKey("currency.id")),

    UniqueConstraint("balance", "user_id"),
)


currency = Table(
    "currency",
    mapper_registry.metadata,
    Column('id', Integer(), primary_key=True),
    Column('currency', String(length=20)),
    Column('country', String(length=20)),
)


class AlchemyUser:
    pass


class AlchemyBalance:
    pass


class AlchemyCurrency:
    pass


mapper_registry.map_imperatively(
    AlchemyUser,
    users,
    properties={
        "balances": relationship(AlchemyBalance, back_populates='user', uselist=True, lazy='select'),
    },
)

mapper_registry.map_imperatively(
    AlchemyBalance,
    balances,
    properties={
        "currency": relationship(AlchemyCurrency, uselist=False, lazy='select'),
        "user": relationship(AlchemyUser, back_populates='balances', lazy='select'),
    },
)

mapper_registry.map_imperatively(AlchemyCurrency, currency)
mapper_registry.metadata.create_all(bind=engine, tables=[users, balances, currency])


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
