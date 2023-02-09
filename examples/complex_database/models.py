from typing import List

from sqlalchemy import create_engine, Column, String, Float, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

from core.database import BaseModel

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
        UniqueConstraint("balance", "currency", "user_id"),
    )

    id = Column(Integer(), primary_key=True)

    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("AlchemyUser", back_populates="balances")

    balance = Column(Float(), server_default='0')
    currency = Column(String(length=20))

    def __str__(self):
        return f"{self.balance} {self.currency}"

    def __repr__(self):
        return str(self)


Base.metadata.create_all(engine)


class InternalBalance(BaseModel):
    balance: float
    currency: str


class InternalUser(BaseModel):
    username: str
    email: str
    balances: List[InternalBalance] = []