from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.database import get_session
from models.tasks import Task
from schemas.tasks import TaskCreationSchema, TaskUpdateSchema


class TaskService:
    """Service for working with tasks.

    Args:
        session (Session): Database session.

    Attributes:
        session (Session): Database session.

    """
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_task(self, pk: int) -> Task:
        task = self.session.query(Task).get(pk)

        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return task

    def get(self, pk: int) -> Task:
        return self._get_task(pk)

    def get_list(self) -> list[Task]:
        return self.session.query(Task).all()

    def create(self, data: TaskCreationSchema) -> Task:
        task = Task(**data.dict())
        self.session.add(task)
        self.session.commit()
        return task

    def update(self, pk: int, data: TaskUpdateSchema) -> Task:
        task = self._get_task(pk)

        for k, v in data:
            setattr(task, k, v)

        self.session.commit()
        return task

    def delete(self, pk: int) -> None:
        task = self._get_task(pk)
        self.session.delete(task)
        self.session.commit()
