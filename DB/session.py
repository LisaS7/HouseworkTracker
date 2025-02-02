from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from config import TESTING, ECHO_LOGS, database_config, IN_DOCKER, platform
from typing import Generator


class Database:
    Base = declarative_base()

    # ---- DB -----
    POSTGRES_USER: str = database_config.user
    POSTGRES_PASSWORD = database_config.password
    POSTGRES_PORT: str = database_config.port
    POSTGRES_DB: str = database_config.db_name

    def __init__(self, in_docker: int = False, platform: str = "linux"):
        self.in_docker = in_docker
        self.platform = platform
        self.POSTGRES_SERVER = self.get_host()

    def get_host(self) -> str:
        if self.in_docker:
            if self.platform.startswith("linux"):
                return database_config.linux_ip
            else:
                return database_config.docker_host
        else:
            return "localhost"

    def set_engine(self, testing: bool) -> sessionmaker:
        if testing:
            self.engine = create_engine(
                "sqlite:///:memory:",
                echo=ECHO_LOGS,
                connect_args={"check_same_thread": False},
            )
        else:
            database_url = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            self.engine = create_engine(database_url, echo=ECHO_LOGS)

        self.Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


database = Database(IN_DOCKER, platform)
database.set_engine(TESTING)


# This function grabs a fresh db connection.
# It closes the connection once it is no longer needed.
def get_db() -> Generator[Session, None, None]:
    session_local = database.get_session()
    db = session_local()
    try:
        yield db
    finally:
        db.close()
