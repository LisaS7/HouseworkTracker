from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from config import settings
from typing import Generator

TESTING = settings.TESTING
ECHO_LOGS = False


def get_engine(testing: int) -> tuple[Engine, sessionmaker]:
    if testing:
        engine = create_engine("sqlite:///:memory:", echo=ECHO_LOGS)
        SessionLocal = sessionmaker(bind=engine)
    else:
        engine = create_engine(settings.DATABASE_URL, echo=ECHO_LOGS)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


engine, SessionLocal = get_engine(TESTING)
Base = declarative_base()


# This function grabs a fresh db connection.
# It closes the connection once it is no longer needed.
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
