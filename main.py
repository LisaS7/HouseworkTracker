from fastapi import FastAPI, Request

from DB.session import engine, Base
from config import settings, templates
from routes import users

from seed import seed


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    Base.metadata.create_all(bind=engine)

    app.include_router(users.router, prefix="/users", tags=["users"])

    return app


app = start_application()
# seed()


@app.get("/")
def main(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")
