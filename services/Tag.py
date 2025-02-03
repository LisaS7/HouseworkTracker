from sqlalchemy.orm import Session
from typing import List

from models.Tag import Tag
from services.schemas import TagCreate, TagUpdate
from config import logger


class TagNotFoundException(Exception):
    def __init__(self, id: int):
        self.message = f"Tag not found for id {id}"
        self.status_code = 404
        logger.error(f"TagNotFoundException: {self.message}")
        super().__init__(self.message)


def get_all_tags(db: Session) -> List[Tag]:
    return db.query(Tag).all()


def get_tag_by_id(db: Session, id: int) -> Tag:
    tag = db.query(Tag).filter(Tag.id == id).first()
    if not tag:
        raise TagNotFoundException(id)
    return tag


def create_tag(db: Session, tag: TagCreate) -> Tag:
    db.add(tag)
    db.commit()
    db.refresh(tag)
    logger.info(f"Created {tag}")
    return tag


def update_tag(db: Session, id: int, tag: TagUpdate) -> Tag:

    existing_tag = get_tag_by_id(db, id)
    logger.info(f"Updating old Tag: {existing_tag}")

    for key, value in tag.items():
        setattr(existing_tag, key, value)

    db.commit()
    db.refresh(existing_tag)
    logger.info(f"Updated to new Tag: {existing_tag}")

    return existing_tag


def delete_tag(db: Session, id: int):
    existing_tag = get_tag_by_id(db, id)
    logger.info(f"Deleting {existing_tag}")
    db.delete(existing_tag)
    db.commit()
