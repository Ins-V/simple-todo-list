from datetime import datetime

from pydantic import BaseModel


class BaseTaskSchema(BaseModel):
    name: str
    description: str


class TaskSchema(BaseTaskSchema):
    id: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class TaskCreationSchema(BaseTaskSchema):
    pass


class TaskUpdateSchema(BaseTaskSchema):
    pass
