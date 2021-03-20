from typing import Optional

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

    def _get_task(self, pk: int, user_id: int) -> Task:
        """Private method for getting one task by id.

        Args:
            pk (int): Task id.
            user_id (int): User id.

        Returns:
            Selected task.
        """
        task = self.session.query(Task).filter_by(id=pk, user_id=user_id).first()

        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return task

    def get(self, pk: int, user_id: int) -> Task:
        """Method for getting one task by id.

        Args:
            pk (int): Task id.
            user_id (int): User id.

        Returns:
            Selected task.
        """
        return self._get_task(pk, user_id)

    def get_list(self, user_id: int, completed: Optional[bool] = None) -> list[Task]:
        """Method for getting a list of tasks.

        There is a way to filter the list by the completed field.

        Args:
            user_id (int): User id.
            completed (:obj: `bool`, optional): Filter by completed.

        Returns:
            Task list.
        """
        filter_by = {'user_id': user_id}
        if completed:
            filter_by.update({'completed': completed})
        return self.session.query(Task).filter_by(**filter_by).all()

    def create(self, data: TaskCreationSchema, user_id: int) -> Task:
        """Task creation method.

        Args:
            data (TaskCreationSchema): Data for a new task.
            user_id (int): User id.

        Returns:
            Created task.
        """
        task = Task(**data.dict(), user_id=user_id)
        self.session.add(task)
        self.session.commit()
        return task

    def update(self, pk: int, data: TaskUpdateSchema, user_id: int) -> Task:
        """Task update method.

        Args:
            pk (int): Task id.
            data (TaskUpdateSchema): Data for updating the task.
            user_id (int): User id.

        Returns:
            Updated task.
        """
        task = self._get_task(pk, user_id)

        for k, v in data:
            setattr(task, k, v)

        self.session.commit()
        return task

    def delete(self, pk: int, user_id: int) -> None:
        """Method for deleting a task.

        Args:
            pk (int): Task id.
            user_id (int): User id.
        """
        task = self._get_task(pk, user_id)
        self.session.delete(task)
        self.session.commit()
