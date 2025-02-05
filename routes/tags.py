from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from typing import List

from config import templates, logger
from DB.session import get_db

from services.Tag import get_all_tags

router = APIRouter()


@router.get("/")
async def get_tags(request: Request, db: Session = Depends(get_db)):
    data = get_all_tags(db)

    print(request.headers.get("accept", ""))
    if "application/json" in request.headers.get("accept", ""):
        return data

    logger.info(f"{request.method} {request.url}")
    return templates.TemplateResponse(
        "/tags/tags.html", context={"request": request, "tags": data}
    )
