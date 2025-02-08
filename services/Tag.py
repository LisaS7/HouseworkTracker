from sqlalchemy.orm import Session
from typing import List

from models.Tag import Tag
from services.schemas import TagCreate, TagUpdate, TagModel
from config import logger


class TagNotFoundException(Exception):
    def __init__(self, id: int):
        self.message = f"Tag not found for id {id}"
        self.status_code = 404
        logger.error(f"TagNotFoundException: {self.message}")
        super().__init__(self.message)


def get_all_tags(db: Session) -> List[TagModel]:
    return db.query(Tag).all()


def get_tag_by_id(db: Session, id: int) -> TagModel:
    tag = db.query(Tag).filter(Tag.id == id).first()
    if not tag:
        raise TagNotFoundException(id)
    return tag


def get_tag_by_name(db: Session, name: str) -> TagModel:
    # ilike makes the query case insensitive! cool!
    tag = db.query(Tag).filter(Tag.name.ilike(name)).first()
    if not tag:
        return None
    return tag


def create_tag(db: Session, tag: TagCreate) -> TagModel:
    # we need to convert pydantic model to sqlalchemy model before adding to db
    new_tag = get_tag_by_name(tag.name)

    if not new_tag:
        db_tag = Tag(name=tag.name)
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        logger.info(f"Created {db_tag}")
        return db_tag
    else:
        return "Tag already exists"


def update_tag(db: Session, id: int, tag_data: TagUpdate) -> TagModel:

    existing_tag = get_tag_by_id(db, id)
    logger.info(f"Updating old Tag: {existing_tag}")

    existing_tag.name = tag_data.name

    db.commit()
    db.refresh(existing_tag)
    logger.info(f"Updated to new Tag: {existing_tag}")

    return existing_tag


def delete_tag(db: Session, id: int):
    existing_tag = get_tag_by_id(db, id)
    logger.info(f"Deleting {existing_tag}")
    db.delete(existing_tag)
    db.commit()
