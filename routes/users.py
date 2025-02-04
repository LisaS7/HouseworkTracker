from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config import templates, logger
from DB.session import get_db
from services.User import get_all_users, create_user

router = APIRouter()


@router.get("/")
async def all_users(request: Request, db: Session = Depends(get_db)):
    data = get_all_users(db)

    accept_header = request.headers.get("Accept", "")

    if "application/json" in accept_header:
        return JSONResponse(content=data)

    logger.info(f"{request.method} {request.url}")

    return templates.TemplateResponse(
        "users.html", context={"request": request, "users": data}
    )
