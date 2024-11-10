from pydantic import BaseModel


class UserData(BaseModel):
    username: str
    email: str
