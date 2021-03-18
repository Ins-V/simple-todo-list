from pathlib import Path

from pydantic import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Base settings project."""
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    database_url: str = f'sqlite:///{BASE_DIR}/db.sqlite3'


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
