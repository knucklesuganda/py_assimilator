import uuid

from sqlalchemy import UUID, String, CheckConstraint, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    transactions_out: Mapped[list['UserTransaction']] = relationship(
        'UserTransaction', back_populates='sender', foreign_keys='UserTransaction.sender_id'
    )
    transactions_in: Mapped[list['UserTransaction']] = relationship(
        'UserTransaction', back_populates='receiver', foreign_keys='UserTransaction.receiver_id'
    )


class UserTransaction(Base):
    __tablename__ = 'users_transactions'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    balance_change: Mapped[float] = mapped_column(Numeric)

    sender_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('users.id'), nullable=False)
    sender: Mapped[User] = relationship('User', foreign_keys=[sender_id], back_populates='transactions_out')

    receiver_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('users.id'), nullable=False)
    receiver: Mapped[User] = relationship('User', foreign_keys=[receiver_id], back_populates='transactions_in')
