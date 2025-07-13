from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from .engine import engine

Base = declarative_base()

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)