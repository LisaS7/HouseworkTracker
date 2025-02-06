from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends

from DB.session import get_db
from config import templates
from services.Task import get_all_overdue_tasks

router = APIRouter()


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    overdue_tasks = get_all_overdue_tasks(db)
    return templates.TemplateResponse(
        name="/home/home.html", context={"request": request, "overdue": overdue_tasks}
    )
