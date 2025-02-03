from datetime import date
from typing import List
from sqlalchemy.orm import Session

from models.Task import Task
from models.Tag import Tag
from services.schemas import TaskCreate, TaskUpdate
from config import logger

TODAY = date.today()


class TaskNotFoundException(Exception):
    def __init__(self, id: int):
        self.message = f"Task not found for id {id}"
        self.status_code = 404
        logger.error(f"TaskNotFoundException: {self.message}")
        super().__init__(self.message)


def get_all_tasks(db: Session) -> List[Task]:
    return db.query(Task).all()


def get_all_incomplete_tasks(db: Session) -> List[Task]:
    return db.query(Task).filter(Task.complete == False).all()


def get_all_overdue_tasks(db: Session) -> List[Task]:
    return db.query(Task).filter(Task.next_due < TODAY).all()


def get_todays_tasks(db: Session) -> List[Task]:
    return db.query(Task).filter(Task.next_due == TODAY).all()


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
    logger.info(f"Created {task}")
    return task


def update_task(db: Session, id: int, task: TaskUpdate) -> Task:
    existing_task = get_task_by_id(db, id)
    logger.info(f"Updating old Task: {existing_task}")

    for key, value in task.items():
        setattr(existing_task, key, value)

    db.commit()
    db.refresh(existing_task)
    logger.info(f"Updated to new Task: {existing_task}")

    return existing_task


def delete_task(db: Session, id: int):
    existing_task = get_task_by_id(db, id)
    logger.info(f"Deleting {existing_task}")
    db.delete(existing_task)
    db.commit()


def add_tags_to_task(db: Session, task: Task, tags: List[Tag]) -> Task:
    logger.info(f"Adding tags {[str(tag) for tag in tags]}")
    logger.info(f"to task {task}")
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
    logger.info(f"Removing tag {tag}")
    logger.info(f"from task {task}")
    if tag in task.tags:
        task.tags.remove(tag)

    db.commit()
    db.refresh(task)
    return task
