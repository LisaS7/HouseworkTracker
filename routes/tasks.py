from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from config import templates, logger
from DB.session import get_db
from services.Task import get_all_tasks, update_task
from services.schemas import PriorityUpdate, TaskUpdate


router = APIRouter()


@router.get("/")
async def all_users(request: Request, db: Session = Depends(get_db)):
    data = get_all_tasks(db)

    logger.info(f"{request.method} {request.url}")
    return templates.TemplateResponse(
        "tasks.html", context={"request": request, "tasks": data}
    )


@router.post("/update-priority/{task_id}")
def update_task_priority(
    task_id: int, data: PriorityUpdate, db: Session = Depends(get_db)
):
    update_task(db, task_id, TaskUpdate(**data.model_dump()))

    return {"message": "Update successful"}
