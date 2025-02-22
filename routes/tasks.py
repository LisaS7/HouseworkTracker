from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from config import templates, logger, PRIORITIES, today
from DB.session import get_db
from services.Task import (
    get_all_tasks,
    get_task_by_id,
    update_task,
    create_task,
    delete_task,
    TaskNotFoundException,
)
from services.User import get_all_users
from services.Tag import get_tag_by_name, get_all_tags
from services.schemas import PriorityUpdate, TaskUpdate, TaskCreate


router = APIRouter()


@router.get("/")
async def get_tasks(request: Request, db: Session = Depends(get_db)):
    data = get_all_tasks(db)

    logger.info(f"{request.method} {request.url}")
    return templates.TemplateResponse(
        "/tasks/tasks.html", context={"request": request, "tasks": data}
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


@router.post("/")
async def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):

    tags = []
    for tag in task.tags:
        existing_tag = get_tag_by_name(db, tag.name)

        if existing_tag:
            tags.append(existing_tag)
        else:
            logger.warning(f"Invalid tag: {tag}")

    task.tags = tags

    # we need to grab the db task to get the id field
    new_task = create_task(db, task)

    return RedirectResponse(url=f"/tasks/{new_task.id}", status_code=201)


@router.patch("/{task_id}/priority")
def update_task_priority(
    task_id: int, data: PriorityUpdate, db: Session = Depends(get_db)
):
    update_task(db, task_id, TaskUpdate(**data.model_dump()))

    return {"message": "Priority update successful"}


@router.patch("/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    data = TaskUpdate(last_completed=today)
    update_task(db, task_id, data)

    return {"message": "Task marked complete"}


@router.put("/{task_id}")
async def edit_task(
    task_id: int, task: TaskUpdate, request: Request, db: Session = Depends(get_db)
):

    new_task = update_task(db, task_id, task)
    logger.info(f"{request.method} {request.url}")
    logger.info(f"Returned {new_task}")
    return RedirectResponse(url=f"/tasks/{new_task.id}", status_code=200)


@router.delete("/{task_id}")
async def task_delete(task_id: int, request: Request, db: Session = Depends(get_db)):
    logger.info(f"{request.method} {request.url}")
    delete_task(db, task_id)
    return RedirectResponse(url="/tasks", status_code=204)


# --------------- FORMS -----------------------


@router.get("/create")
async def create_task_form(request: Request, db: Session = Depends(get_db)):
    users = get_all_users(db)
    tags = get_all_tags(db)
    logger.info(f"{request.method} {request.url}")
    return templates.TemplateResponse(
        "/tasks/task_form.html",
        context={
            "request": request,
            "priorities": PRIORITIES,
            "users": users,
            "tags": tags,
        },
    )


@router.get("/{task_id}/edit")
async def edit_task_form(task_id: int, request: Request, db: Session = Depends(get_db)):
    task = get_task_by_id(db, task_id)
    tag_names = [tag.name for tag in task.tags]
    users = get_all_users(db)
    tags = get_all_tags(db)

    logger.info(f"{request.method} {request.url}")
    return templates.TemplateResponse(
        "/tasks/task_form.html",
        context={
            "request": request,
            "task": task,
            "tag_names": tag_names,
            "priorities": PRIORITIES,
            "users": users,
            "tags": tags,
        },
    )
