from pathlib import Path

from pydantic import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Base settings project."""
    server_host: str
    server_port: int
    database_url: str
    secret_key: str
    crypt_algorithm: str
    token_expires: int


settings = Settings(
    _env_file=BASE_DIR / '.env',
    _env_file_encoding='utf-8'
)
