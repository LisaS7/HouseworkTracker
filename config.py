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

    # ---- DB -----
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_PORT: str = os.getenv(
        "POSTGRES_PORT", 5432
    )  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "housework")

    # Determine Host
    if os.getenv("IN_DOCKER") == True:
        if sys.platform.startswith("linux"):
            os.getenv("LINUX_IP")
        else:
            POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    else:
        POSTGRES_SERVER: str = "localhost"

    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # ---- MODELS -----
    MAX_TITLE_LENGTH: int = 255


settings = Settings()
