from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class OrderStatus(Base):
    __tablename__ = "order_statuses"
    id = Column(Integer(), primary_key=True)
    status = Column(String(), unique=True)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())

    product_name = Column(String())
    price = Column(Float())

    status_id = Column(
        Integer(),
        ForeignKey(column="order_statuses.id", ondelete='CASCADE'),
        nullable=False,
    )
    order_status = relationship('OrderStatus', uselist=False)
