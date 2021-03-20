from datetime import datetime

from pydantic import BaseModel


class BaseUserSchema(BaseModel):
    username: str
    email: str


class UserCreationSchema(BaseUserSchema):
    password: str


class UserSchema(BaseUserSchema):
    id: int
    created: datetime

    class Config:
        orm_mode = True
