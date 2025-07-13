from sqlalchemy import create_engine
from app import settings

DATABASE_URL = (
    f"{settings.DB_DIALECT}+{settings.DB_DRIVER}://{settings.DB_USER}:{settings.DB_PASSWD}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?charset=utf8"
)

engine = create_engine(DATABASE_URL, echo=True)