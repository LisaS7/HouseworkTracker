from pydantic import BaseModel
from sqlalchemy.orm import Session
from models.Task import Task, Priority
from datetime import date
from typing import List

TODAY = date.today()


class TaskNotFoundException(Exception):
    def __init__(self, id: int):
        self.message = f"Task not found for id {id}"
        self.status_code = 404
        super().__init__(self.message)


class TaskModel(BaseModel):
    id: int
    title: str
    priority: Priority
    due_date: date
    complete: bool
    user_id: int


class TaskCreate(BaseModel):
    title: str
    priority: Priority | None = Priority.LOW
    due_date: date | None = None
    complete: bool | None = False
    user_id: int


class TaskUpdate(BaseModel):
    title: str | None
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

    return task


def delete_task(db: Session, id: int):
    existing_task = get_task_by_id(db, id)
    db.delete(existing_task)
    db.commit()
