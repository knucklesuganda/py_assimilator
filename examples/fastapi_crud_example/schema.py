from typing import List

from pydantic import BaseModel


class CurrencySchema(BaseModel):
    currency: str
    country: str


class BalanceSchema(BaseModel):
    balance: int
    currency: CurrencySchema


class UserSchema(BaseModel):
    username: str
    balances: List[BalanceSchema]
