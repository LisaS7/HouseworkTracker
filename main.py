from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException

from DB.session import database
from config import templates, PROJECT_NAME, PROJECT_VERSION, TESTING
from routes import users, tasks

# These imports aren't used here but importing them ensures the models are defined in the correct order
from models.Task import Task
from models.Tag import Tag
from models.User import User


app = FastAPI(title=PROJECT_NAME, version=PROJECT_VERSION)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])


if not TESTING:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    database.set_engine(testing=TESTING)


@app.exception_handler(HTTPException)
async def custom_404_error(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {"request": request})
    else:
        # For other exceptions
        raise exc


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="/home/home.html")
