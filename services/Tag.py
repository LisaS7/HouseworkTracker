from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from services.Task import TaskModel
from models.Tag import Tag


class TagNotFoundException(Exception):
    def __init__(self, id: int):
        self.message = f"Tag not found for id {id}"
        self.status_code = 404
        super().__init__(self.message)


class TagModel(BaseModel):
    id: int
    name: str
    tasks: List[TaskModel]


class TagCreate(BaseModel):
    name: str | None


class TagUpdate(BaseModel):
    name: str


def get_all_tags(db: Session) -> List[Tag]:
    return db.query(Tag).all()


def get_tag_by_id(db: Session, id: int) -> Tag:
    tag = db.query(Tag).filter(Tag.id == id).first()
    if not tag:
        raise TagNotFoundException(id)
    return tag


def get_tags_by_task() -> List[Tag]:
    pass


def create_tag(db: Session, tag: TagCreate) -> Tag:
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def update_tag(db: Session, id: int, tag: TagUpdate) -> Tag:
    existing_tag = get_tag_by_id(db, id)

    for key, value in tag.items():
        setattr(existing_tag, key, value)

    db.commit()
    db.refresh(existing_tag)

    return existing_tag


def delete_tag(db: Session, id: int):
    existing_tag = get_tag_by_id(db, id)
    db.delete(existing_tag)
    db.commit()
