from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from schemas.users import UserCreationSchema
from schemas.tokens import TokenSchema
from services.auth import AuthService


router = APIRouter(prefix='/auth')


@router.post('/login/', response_model=TokenSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          service: AuthService = Depends()):
    return service.login(form_data.username, form_data.password)


@router.post('/registration/', response_model=TokenSchema)
def registration(user_data: UserCreationSchema,
                 service: AuthService = Depends()):
    return service.registration(user_data)
