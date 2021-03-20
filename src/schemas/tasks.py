from datetime import datetime

from pydantic import BaseModel


class BaseTaskSchema(BaseModel):
    name: str
    description: str


class TaskCompletedSchema(BaseModel):
    completed: bool


class TaskSchema(TaskCompletedSchema, BaseTaskSchema):
    id: int
    created: datetime
    updated: datetime
    completed: bool

    class Config:
        orm_mode = True


class TaskCreationSchema(BaseTaskSchema):
    pass


class TaskUpdateSchema(TaskCompletedSchema, BaseTaskSchema):
    pass
