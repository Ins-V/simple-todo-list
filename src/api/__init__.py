from fastapi import APIRouter

from api.auth import router as auth_router
from api.tasks import router as task_router


router = APIRouter()
router.include_router(auth_router)
router.include_router(task_router)
