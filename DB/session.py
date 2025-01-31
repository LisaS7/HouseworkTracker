import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from config import settings
from typing import Generator

if settings.TESTING:
    engine = create_engine("sqlite:///:memory:", echo=True)
    SessionLocal = sessionmaker(bind=engine)
else:
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# This function grabs a fresh db connection.
# It closes the connection once it is no longer needed.
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
