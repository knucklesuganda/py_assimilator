from assimilator.core.events.events import Event


class UserCreated(Event):
    user_id: int
    username: str
    email: str
    balance: float


class UserBilled(Event):
    user_id: int
    order_id: int
    success: bool


class OrderCreated(Event):
    order_id: int
    user_id: int
    status: str
    price: int


class OrderStatusChanged(Event):
    order_id: int
    new_status: str
