from typing import List

from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True


class CurrencySchema(BaseSchema):
    currency: str
    country: str


class BalanceSchema(BaseSchema):
    balance: int
    currency: CurrencySchema


class UserSchema(BaseSchema):
    username: str
    balances: List[BalanceSchema]
