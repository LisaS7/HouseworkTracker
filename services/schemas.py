from datetime import date
from typing import List
from pydantic import BaseModel, Field, EmailStr
from models.Task import Priority

from config import MAX_TAG_LENGTH, MAX_TITLE_LENGTH

# ----------- TAGS -----------


class TagModel(BaseModel):
    id: int
    name: str = Field(
        ...,
        min_length=1,
        max_length=MAX_TAG_LENGTH,
        description=f"Tag name (1-{MAX_TAG_LENGTH} characters)",
    )


class TagCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=MAX_TAG_LENGTH,
        description=f"Tag name (1-{MAX_TAG_LENGTH} characters)",
    )


class TagUpdate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=MAX_TAG_LENGTH,
        description=f"Tag name (1-{MAX_TAG_LENGTH} characters)",
    )


# ----------- TASKS -----------


class TaskModel(BaseModel):
    id: int
    title: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description=f"Title of the task (3-{MAX_TITLE_LENGTH} characters)",
    )
    priority: Priority
    last_completed: date | None = Field(
        None, description="Date the task was last completed"
    )
    repeat_interval: int = Field(
        0, description="The number of days between repeat tasks"
    )
    user_id: int


class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description=f"Title of the task (3-{MAX_TITLE_LENGTH} characters)",
    )
    priority: Priority | None = Priority.LOW
    last_completed: date | None = None
    repeat_interval: int | None = None
    user_id: int
    tags: List[TagModel] | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(
        None,
        min_length=3,
        max_length=255,
        description=f"Title of the task (3-{MAX_TITLE_LENGTH} characters)",
    )
    priority: Priority | None
    last_completed: date | None = None
    repeat_interval: int | None = None
    user_id: int
    tags: List[TagModel] | None = None


# ----------- USERS -----------


class UserModel(BaseModel):
    id: int
    name: str
    email: EmailStr
    active: bool


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    name: str | None
    email: EmailStr | None
    active: bool | None
