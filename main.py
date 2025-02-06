from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from DB.session import database
from config import templates, PROJECT_NAME, PROJECT_VERSION, TESTING
from routes import users, tasks, tags, home

# These imports aren't used here but importing them ensures the models are defined in the correct order
from models.Task import Task
from models.Tag import Tag
from models.User import User


# ----------------- SETUP -----------------

app = FastAPI(title=PROJECT_NAME, version=PROJECT_VERSION)

app.include_router(home.router, tags=["home"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])

if not TESTING:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    database.set_engine(testing=TESTING)

# ----------------- HANDLING ERRORS -----------------


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation failed", "errors": exc.errors()},
    )


@app.exception_handler(HTTPException)
async def custom_404_error(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "404.html", {"request": request, "detail": exc.detail}
        )
    else:
        # For other exceptions
        raise exc
