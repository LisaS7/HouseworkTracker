from datetime import date, timedelta
from typing import List
from sqlalchemy.orm import Session

from models.Task import Task
from services.schemas import TaskCreate, TaskUpdate, TaskModel, TagModel
from services.Tag import get_tag_by_name
from config import logger

TODAY = date.today()


class TaskNotFoundException(Exception):
    def __init__(self, id: int):
        self.message = f"Task not found for id {id}"
        self.status_code = 404
        logger.error(f"TaskNotFoundException: {self.message}")
        super().__init__(self.message)


def get_all_tasks(db: Session) -> List[TaskModel]:
    return db.query(Task).all()


def get_all_overdue_tasks(db: Session) -> List[TaskModel]:
    return db.query(Task).filter(Task.next_due < TODAY).all()


def get_todays_tasks(db: Session) -> List[TaskModel]:
    return db.query(Task).filter(Task.next_due == TODAY).all()


def get_week_tasks(db: Session) -> List[TaskModel]:
    next_week = TODAY + timedelta(days=7)
    return (
        db.query(Task)
        .filter(
            Task.next_due > TODAY,  # Exclude today
            Task.next_due <= next_week,  # Include up to 7 days ahead
        )
        .all()
    )


def get_tasks_by_user(db: Session, id: int) -> List[TaskModel]:
    return db.query(Task).filter(Task.user_id == id).all()


def get_task_by_id(db: Session, id: int) -> TaskModel:
    task = db.query(Task).filter(Task.id == id).first()
    if not task:
        raise TaskNotFoundException(id)
    return task


def create_task(db: Session, task: TaskCreate) -> TaskModel:
    db_task = Task(
        title=task.title,
        priority=task.priority,
        last_completed=task.last_completed,
        repeat_interval=task.repeat_interval,
        user_id=task.user_id,
        tags=task.tags,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    logger.info(f"Created {db_task}")
    return db_task


def update_task(db: Session, id: int, task: TaskUpdate) -> TaskModel:
    existing_task = get_task_by_id(db, id)
    logger.info(f"Updating old Task: {existing_task}")

    task_data = task.model_dump(exclude_unset=True)

    # Loop over each field in the data and set it on the task object
    for key, value in task_data.items():
        # If tags then we need to check whether they exist already
        if key == "tags":
            tags = []
            for tag in value:
                existing_tag = get_tag_by_name(db, tag["name"])

            if existing_tag:
                tags.append(existing_tag)
            else:
                logger.warning(f"Invalid tag: {tag}")

            # set the tags to our new list
            existing_task.tags = tags
        else:
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


def add_tags_to_task(db: Session, task: Task, tags: List[TagModel]) -> Task:
    logger.info(f"Adding tags {[str(tag) for tag in tags]}")
    logger.info(f"to task {task}")
    for tag in tags:
        if tag not in task.tags:
            task.tags.append(tag)

    db.commit()
    db.refresh(task)
    return task


def get_tags_by_task(db: Session, id: int) -> List[TagModel] | None:
    task = get_task_by_id(db, id)
    return task.tags if task.tags else None


def get_tasks_by_tag(db: Session, tag: TagModel) -> List[Task] | None:
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
