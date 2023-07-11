from pydantic import BaseModel


class OrderCreateSchema(BaseModel):
    product_name: str
    quantity: float
    price: float
