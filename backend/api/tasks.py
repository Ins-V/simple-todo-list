from fastapi import APIRouter, Depends, Response, status

from schemas.tasks import TaskSchema, TaskCreationSchema, TaskUpdateSchema
from services.tasks import TaskService


router = APIRouter(prefix='/task')


@router.get('/list/', response_model=list[TaskSchema])
def get_task_list(service: TaskService = Depends()):
    return service.get_list()


@router.get('/{pk}/', response_model=TaskSchema)
def get_task(pk: int, service: TaskService = Depends()):
    return service.get(pk)


@router.post('/', response_model=TaskSchema)
def create_task(data: TaskCreationSchema, service: TaskService = Depends()):
    return service.create(data)


@router.put('/{pk}/', response_model=TaskSchema)
def update_task(pk: int, data: TaskUpdateSchema, service: TaskService = Depends()):
    return service.update(pk, data)


@router.delete('/{pk}/')
def delete_task(pk: int, service: TaskService = Depends()):
    service.delete(pk)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
