import os, sys
import logging
from dataclasses import dataclass
from datetime import date
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from pathlib import Path

# ----- ENV VARIABLES ------
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

TESTING = os.getenv("TESTING")


# ----- PROJECT ------
PROJECT_NAME = "Housework Tracker"
PROJECT_VERSION = "1.0.0"

# ----- CONFIGS ------
MAX_TITLE_LENGTH = 255
MAX_TAG_LENGTH = 50
MAX_USER_NAME_LENGTH = 50

PRIORITIES = ("LOW", "MEDIUM", "HIGH")


# Database
@dataclass
class DatabaseConfig:
    user: str
    password: str
    port: str
    db_name: str
    server: str = None

    def __post_init__(self):
        IN_DOCKER = os.getenv("IN_DOCKER")
        if IN_DOCKER:
            self.server = os.getenv("DOCKER_HOST")
        else:
            self.server = "localhost"


database_config = DatabaseConfig(
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("POSTGRES_PORT", 5432),
    db_name=os.getenv("POSTGRES_DB", "housework"),
)


# ----- TEMPLATES ------
templates = Jinja2Templates(directory="templates")


# ----- LOGGING ------
LOG_LEVEL = logging.INFO
LOG_DIR = "logs"
ECHO_LOGS = False

today = date.today()
os.makedirs(LOG_DIR, exist_ok=True)

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
