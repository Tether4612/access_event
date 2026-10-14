import os

from dotenv import load_dotenv

# Читаем файл .env (если он есть) ДО обращения к os.environ.
# Без этой строки DATABASE_URL и SECRET_KEY из .env не подхватываются.
load_dotenv()


def _database_url():
    url = os.environ.get("DATABASE_URL", "sqlite:///accessevent.db")
    # Старый формат postgres:// SQLAlchemy не понимает
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "dev-secret-key-for-accessevent-at-least-32-bytes"
    )
    # Сначала PostgreSQL из .env; если переменной нет - запасной SQLite
    SQLALCHEMY_DATABASE_URI = _database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_HOURS = 24
