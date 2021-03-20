from typing import Optional

from fastapi import APIRouter, Depends, Response, status

from schemas.tasks import TaskSchema, TaskCreationSchema, TaskUpdateSchema
from services.tasks import TaskService
from models.users import User
from services.auth import get_current_user


router = APIRouter(prefix='/task', tags=['tasks'])


@router.get('/list/', response_model=list[TaskSchema])
def get_task_list(user: User = Depends(get_current_user),
                  completed: Optional[bool] = None,
                  service: TaskService = Depends()):
    return service.get_list(user.id, completed)


@router.get('/{pk}/', response_model=TaskSchema)
def get_task(pk: int,
             user: User = Depends(get_current_user),
             service: TaskService = Depends()):
    return service.get(pk, user.id)


@router.post('/', response_model=TaskSchema)
def create_task(data: TaskCreationSchema,
                user: User = Depends(get_current_user),
                service: TaskService = Depends()):
    return service.create(data, user.id)


@router.put('/{pk}/', response_model=TaskSchema)
def update_task(pk: int,
                data: TaskUpdateSchema,
                user: User = Depends(get_current_user),
                service: TaskService = Depends()):
    return service.update(pk, data, user.id)


@router.delete('/{pk}/')
def delete_task(pk: int,
                user: User = Depends(get_current_user),
                service: TaskService = Depends()):
    service.delete(pk, user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
