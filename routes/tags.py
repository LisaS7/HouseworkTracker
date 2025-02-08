from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session

from config import templates, logger
from DB.session import get_db

from services.Tag import (
    get_all_tags,
    get_tag_by_name,
    create_tag,
    delete_tag,
    update_tag,
)
from services.schemas import TagCreate, TagUpdate

router = APIRouter()


@router.get("/")
async def get_tags(request: Request, db: Session = Depends(get_db)):
    data = get_all_tags(db)

    if "application/json" in request.headers.get("accept", ""):
        return data

    logger.info(f"{request.method} {request.url}")
    return templates.TemplateResponse(
        "/tags/tags.html", context={"request": request, "tags": data}
    )


@router.post("/")
async def create_new_tag(
    request: Request, tag: TagCreate, db: Session = Depends(get_db)
):
    logger.info(f"{request.method} {request.url}")
    existing = get_tag_by_name(db, tag.name)

    if not existing:
        create_tag(db, tag)
    else:
        logger.warning(f"Tag already exists: {tag}")
        return JSONResponse(status_code=409, content="Tag already exists")

    return RedirectResponse(url="/tags", status_code=201)


@router.delete("/{tag_id}")
async def tag_delete(tag_id: int, db: Session = Depends(get_db)):
    delete_tag(db, tag_id)
    return RedirectResponse(url="/tags", status_code=204)


# TODO: edit tags
@router.put("/{tag_id}")
async def edit_tag_name(
    request: Request, tag_id: int, tag: TagUpdate, db: Session = Depends(get_db)
):
    logger.info(f"{request.method} {request.url}")
    existing = get_tag_by_name(db, tag.name)

    # check if we already have a tag by that name
    if existing:
        logger.warning(f"Tag already exists: {tag}")
        return JSONResponse(status_code=409, content="Tag already exists")
    else:
        update_tag(db, tag_id, tag)
