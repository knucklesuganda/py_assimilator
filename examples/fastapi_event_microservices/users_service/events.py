from assimilator.core.events.events import Event


class UserCreated(Event):
    user_id: int
    username: str
    email: str
    balance: float
