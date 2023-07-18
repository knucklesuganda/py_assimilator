from pydantic import BaseModel


class OrderCreateSchema(BaseModel):
    product_name: str
    price: float
    user_id: int
