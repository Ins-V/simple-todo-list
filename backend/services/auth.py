from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, IntegrityError
from jose import jwt, JWTError
from passlib.hash import bcrypt

from config.database import get_session
from config.settings import settings
from models.users import User
from schemas.users import UserSchema, UserCreationSchema
from schemas.tokens import TokenSchema


class AuthService:
    """User authorization and registration service.

    The service allows you to create a new user and authorize an existing one.
    It also implements verification of transferred tokens and creates new tokens.

    Args:
        session (Session): Database session.

    Attributes:
        session (Session): Database session.

    """
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    @classmethod
    def verify_password(cls, raw_password: str, hash_password: str) -> bool:
        """Password verification method.

        Args:
            raw_password (str): The raw password sent from the client.
            hash_password (str): The hash of the password stored in the database.

        Returns:
            bool: True if the password has been verified, False otherwise.
        """
        return bcrypt.verify(raw_password, hash_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Password encryption method.

        Args:
            password (str): Raw password.

        Returns:
            str: Hash of password.
        """
        return bcrypt.hash(password)

    @classmethod
    def check_token(cls, token: str) -> User:
        """Validates the passed token and returns a user instance if the token is valid.

        Args:
            token (str): Token

        Returns:
            User instance.

        Raises:
            HTTPException: If token invalid.
        """
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )

        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.crypt_algorithm])
        except JWTError:
            raise exception from None

        user_id = payload.get('user_id')

        try:
            user = User.query.get(user_id)
        except NoResultFound:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: User) -> TokenSchema:
        """Token creation method.

        Args:
            user (User): User model instance.

        Returns:
            The created token object.
        """
        user_data = UserSchema.from_orm(user)
        now = datetime.utcnow()

        token = jwt.encode(
            {
                'iat': now,
                'nbf': now,
                'exp': now + timedelta(seconds=300),
                'sub': str(user_data.id),
                'user_id': str(user_data.id)
            },
            settings.secret_key,
            algorithm=settings.crypt_algorithm
        )

        return TokenSchema(access_token=token)

    def authenticate(self, username: str, password: str) -> User:
        """User authentication method.

        Args:
            username (str): Username
            password (str): Raw password.

        Returns:
            User instance.

        Raises:
            HTTPException: If authentication failed.
        """
        user = self.session.query(User).filter(User.username == username).first()

        if not user or not self.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect username or password',
                headers={'WWW-Authenticate': 'Bearer'}
            )

        return user

    def login(self, username: str, password: str) -> TokenSchema:
        """Checks if the user exists and creates a token for him.

        Args:
            username (str): Username
            password (str): Raw password

        Returns:
            User token.
        """
        user = self.authenticate(username, password)
        return self.create_token(user)

    def registration(self, user_data: UserCreationSchema) -> TokenSchema:
        """Create a new user.

        Args:
            user_data (UserCreationSchema): Data for creating a new user.

        Returns:
            User token.
        """
        try:
            user = User(
                username=user_data.username,
                password=self.hash_password(user_data.password),
                email=user_data.email
            )
            self.session.add(user)
            self.session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='This user is already registered.'
            )

        return self.create_token(user)
