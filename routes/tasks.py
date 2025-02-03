from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from config import templates, logger
from DB.session import get_db
from services.Task import get_all_tasks
from models.Task import Priority


router = APIRouter()


@router.get("/")
async def all_users(request: Request, db: Session = Depends(get_db)):
    data = get_all_tasks(db)

    logger.info(f"{request.method} {request.url}")

    return templates.TemplateResponse(
        "tasks.jinja", context={"request": request, "tasks": data, "Priority": Priority}
    )
