from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from config import TESTING, ECHO_LOGS, database_config, logger
from typing import Generator


class Database:
    Base = declarative_base()

    # ---- DB -----
    POSTGRES_USER: str = database_config.user
    POSTGRES_PASSWORD = database_config.password
    POSTGRES_PORT: str = database_config.port
    POSTGRES_DB: str = database_config.db_name
    POSTGRES_SERVER: str = database_config.server

    def set_engine(self, testing: bool) -> sessionmaker:
        if testing:
            self.engine = create_engine(
                "sqlite:///:memory:",
                echo=ECHO_LOGS,
                connect_args={"check_same_thread": False},
            )
        else:
            database_url = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            logger.info(f"CONNECTING:    {database_url}")
            self.engine = create_engine(database_url, echo=ECHO_LOGS)

        try:
            self.Base.metadata.create_all(bind=self.engine)
            logger.info("Tables created successfully.")
        except OperationalError as e:
            logger.error(f"Error creating tables: {e}")

    def get_session(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


database = Database()
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
