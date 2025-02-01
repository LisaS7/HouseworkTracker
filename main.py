from fastapi import FastAPI, Request

from DB.session import engine, Base
from config import templates, PROJECT_NAME, PROJECT_VERSION
from routes import users

from seed import seed


app = FastAPI(title=PROJECT_NAME, version=PROJECT_VERSION)
Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users", tags=["users"])


# seed()


@app.get("/")
def main(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")
