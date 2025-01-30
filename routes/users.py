from fastapi import APIRouter, Request
from config import templates

router = APIRouter()


@router.get("/")
async def all_users(request: Request):
    return templates.TemplateResponse(request=request, name="users.html")
