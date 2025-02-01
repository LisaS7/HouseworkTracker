import os, sys
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from pathlib import Path

templates = Jinja2Templates(directory="templates")

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    # ---- PROJECT -----
    PROJECT_NAME: str = "Housework Tracker"
    PROJECT_VERSION: str = "1.0.0"
    TESTING: int = os.getenv("TESTING")

    # ---- DB -----
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_PORT: str = os.getenv(
        "POSTGRES_PORT", 5432
    )  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "housework")

    # ---- MODELS -----
    MAX_TITLE_LENGTH = 255
    MAX_TAG_LENGTH = 50
    MAX_USER_NAME_LENGTH = 50

    def __init__(self, in_docker: int, platform: str):
        self.in_docker = in_docker
        self.platform = platform
        self.POSTGRES_SERVER = self.get_host()
        self.DATABASE_URL = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def get_host(self) -> str:
        if self.in_docker:
            print("in docker!")
            if self.platform.startswith("linux"):
                print("is linux!")
                return os.getenv("LINUX_IP")
            else:
                return os.getenv("POSTGRES_SERVER")
        else:
            return "localhost"


in_docker = os.getenv("IN_DOCKER")
platform = sys.platform
settings = Settings(in_docker, platform)
