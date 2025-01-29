from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

app = FastAPI()

print(settings.DATABASE_URL)
engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/")
def main():
    print(engine)
    print(SessionLocal)
    return {"message": "Hello, World!"}
