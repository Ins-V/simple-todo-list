from datetime import datetime

from pydantic import BaseModel


class BaseUserSchema(BaseModel):
    name: str
    email: str


class UserCreationSchema(BaseUserSchema):
    password: str


class UserSchema(BaseUserSchema):
    id: int
    created: datetime
