import os, sys
import logging
from datetime import date
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from pathlib import Path

# ----- ENV VARIABLES ------
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

TESTING = os.getenv("TESTING")
IN_DOCKER = os.getenv("IN_DOCKER")


# ----- PROJECT ------
PROJECT_NAME = "Housework Tracker"
PROJECT_VERSION = "1.0.0"
platform = sys.platform

# ----- CONFIGS ------
MAX_TITLE_LENGTH = 255
MAX_TAG_LENGTH = 50
MAX_USER_NAME_LENGTH = 50

# ----- TEMPLATES ------
templates = Jinja2Templates(directory="templates")


# ----- LOGGING ------
LOG_LEVEL = logging.INFO
ECHO_LOGS = False
today = date.today()

logger = logging.getLogger(__name__)

if TESTING:
    filepath = f"logs/housework_tracker_test_{today.strftime('%Y-%m-%d')}.log"
else:
    filepath = f"logs/housework_tracker_{today.strftime('%Y-%m-%d')}.log"

logging.basicConfig(
    level=LOG_LEVEL,
    handlers=[
        logging.FileHandler(filepath, mode="a"),
        logging.StreamHandler(),
    ],
)


class Database:

    # ---- DB -----
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_PORT: str = os.getenv(
        "POSTGRES_PORT", 5432
    )  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "housework")

    def __init__(self, in_docker: int, platform: str):
        self.in_docker = in_docker
        self.platform = platform
        self.POSTGRES_SERVER = self.get_host()
        self.DATABASE_URL = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def get_host(self) -> str:
        if self.in_docker:
            if self.platform.startswith("linux"):
                return os.getenv("LINUX_IP")
            else:
                return os.getenv("DOCKER_HOST")
        else:
            return "localhost"


settings = Database(IN_DOCKER, platform)
