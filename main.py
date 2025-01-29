from fastapi import FastAPI
from DB.session import engine
from DB.base import Base
from config import settings


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    return app


app = start_application()


@app.get("/")
def main():
    return {"message": "Hello, World!"}
