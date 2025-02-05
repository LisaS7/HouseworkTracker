from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from config import templates, logger, PRIORITIES
from DB.session import get_db
from services.Task import (
    get_all_tasks,
    get_task_by_id,
    update_task,
    TaskNotFoundException,
)
from services.User import get_all_users
from services.schemas import PriorityUpdate, TaskUpdate


router = APIRouter()


@router.get("/")
async def get_tasks(request: Request, db: Session = Depends(get_db)):
    data = get_all_tasks(db)

    logger.info(f"{request.method} {request.url}")
    return templates.TemplateResponse(
        "/tasks/tasks.html", context={"request": request, "tasks": data}
    )


@router.post("/")
async def create_task():
    # get request body

    # add any tags that don't already exist

    # validate with pydantic

    # call services function

    # redirect to /tasks

    pass


@router.get("/create")
async def create_task_form(request: Request, db: Session = Depends(get_db)):
    users = get_all_users(db)
    logger.info(f"{request.method} {request.url}")
    return templates.TemplateResponse(
        "/tasks/task_form.html",
        context={"request": request, "priorities": PRIORITIES, "users": users},
    )


@router.get("/{task_id}")
async def get_task(task_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        task = get_task_by_id(db, task_id)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

    logger.info(f"{request.method} {request.url}")
    logger.info(f"Returned {task}")
    return templates.TemplateResponse(
        "/tasks/task_detail.html", context={"request": request, "task": task}
    )


@router.patch("/{task_id}/priority")
def update_task_priority(
    task_id: int, data: PriorityUpdate, db: Session = Depends(get_db)
):
    update_task(db, task_id, TaskUpdate(**data.model_dump()))

    return {"message": "Priority update successful"}


@router.put("/{task_id}")
async def edit_task(task_id: int, request: Request, db: Session = Depends(get_db)):
    task = get_task_by_id(db, task_id)

    logger.info(f"{request.method} {request.url}")
    logger.info(f"Returned {task}")
    return templates.TemplateResponse(
        "/tasks/task_detail.html", context={"request": request, "task": task}
    )


@router.delete("/{task_id}")
async def delete_task(task_id: int, request: Request, db: Session = Depends(get_db)):
    task = get_task_by_id(db, task_id)

    logger.info(f"{request.method} {request.url}")
    logger.info(f"Task to delete: {task}")
    return RedirectResponse(url="/tasks", status_code=204)
