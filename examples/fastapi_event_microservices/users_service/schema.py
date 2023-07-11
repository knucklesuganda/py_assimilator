from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: str
    email: str
