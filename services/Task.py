from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models.Task import Task, Priority
from models.Tag import Tag
from datetime import date
from typing import List
from config import logger, MAX_TITLE_LENGTH

TODAY = date.today()


class TaskNotFoundException(Exception):
    def __init__(self, id: int):
        self.message = f"Task not found for id {id}"
        self.status_code = 404
        logger.error(f"TaskNotFoundException: {self.message}")
        super().__init__(self.message)


class TaskModel(BaseModel):
    id: int
    title: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description=f"Title of the task (3-{MAX_TITLE_LENGTH} characters)",
    )
    priority: Priority
    due_date: date | None = Field(None, description="Due date of the task")
    complete: bool = Field(False, description="Indicates if the task is complete")
    user_id: int


class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description=f"Title of the task (3-{MAX_TITLE_LENGTH} characters)",
    )
    priority: Priority | None = Priority.LOW
    due_date: date | None = None
    complete: bool | None = False
    user_id: int


class TaskUpdate(BaseModel):
    title: str | None = Field(
        None,
        min_length=3,
        max_length=255,
        description=f"Title of the task (3-{MAX_TITLE_LENGTH} characters)",
    )
    priority: Priority | None
    due_date: date | None
    complete: bool | None
    user_id: int


def get_all_tasks(db: Session) -> List[Task]:
    return db.query(Task).all()


def get_all_incomplete_tasks(db: Session) -> List[Task]:
    return db.query(Task).filter(Task.complete == False).all()


def get_all_overdue_tasks(db: Session) -> List[Task]:
    return db.query(Task).filter(Task.due_date < TODAY, Task.complete == False).all()


def get_todays_tasks(db: Session) -> List[Task]:
    return db.query(Task).filter(Task.due_date == TODAY, Task.complete == False).all()


def get_tasks_by_user(db: Session, id: int) -> List[Task]:
    return db.query(Task).filter(Task.user_id == id).all()


def get_task_by_id(db: Session, id: int) -> Task:
    task = db.query(Task).filter(Task.id == id).first()
    if not task:
        raise TaskNotFoundException(id)
    return task


def create_task(db: Session, task: TaskCreate) -> Task:
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, id: int, task: TaskUpdate) -> Task:
    existing_task = get_task_by_id(db, id)

    for key, value in task.items():
        setattr(existing_task, key, value)

    db.commit()
    db.refresh(existing_task)

    return existing_task


def delete_task(db: Session, id: int):
    existing_task = get_task_by_id(db, id)
    db.delete(existing_task)
    db.commit()


def add_tags_to_task(db: Session, task: Task, tags: List[Tag]) -> Task:
    for tag in tags:
        if tag not in task.tags:
            task.tags.append(tag)

    db.commit()
    db.refresh(task)
    return task


def get_tags_by_task(db: Session, id: int) -> List[Tag] | None:
    task = get_task_by_id(db, id)
    return task.tags if task.tags else None


def get_tasks_by_tag(db: Session, tag: Tag) -> List[Task] | None:
    db.refresh(tag)  # ensures the relationship is loaded
    return tag.tasks if tag.tasks else None


def remove_tag_from_task(db: Session, id: int, tag) -> Task:
    task = get_task_by_id(db, id)

    if tag in task.tags:
        task.tags.remove(tag)

    db.commit()
    db.refresh(task)
    return task
