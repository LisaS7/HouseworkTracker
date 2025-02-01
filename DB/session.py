from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from config import TESTING, ECHO_LOGS, database_config, IN_DOCKER, platform
from typing import Generator


class Database:

    # ---- DB -----
    POSTGRES_USER: str = database_config.user
    POSTGRES_PASSWORD = database_config.password
    POSTGRES_PORT: str = database_config.port
    POSTGRES_DB: str = database_config.db_name

    def __init__(self, in_docker: int = False, platform: str = "linux"):
        self.in_docker = in_docker
        self.platform = platform
        self.POSTGRES_SERVER = self.get_host()
        self.DATABASE_URL = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

        self.session = None

    def get_host(self) -> str:
        if self.in_docker:
            if self.platform.startswith("linux"):
                return database_config.linux_ip
            else:
                return database_config.docker_host
        else:
            return "localhost"

    def get_engine(self, testing: int) -> tuple[Engine, sessionmaker]:
        if testing:
            engine = create_engine("sqlite:///:memory:", echo=ECHO_LOGS)
            self.session = sessionmaker(bind=engine)
        else:
            engine = create_engine(self.DATABASE_URL, echo=ECHO_LOGS)
            self.session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return engine, self.session


database = Database(IN_DOCKER, platform)

engine, SessionLocal = database.get_engine(TESTING)
Base = declarative_base()


# This function grabs a fresh db connection.
# It closes the connection once it is no longer needed.
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
