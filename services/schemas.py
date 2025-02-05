from datetime import date
from typing import List
from pydantic import BaseModel, Field, EmailStr

from config import MAX_TAG_LENGTH, MAX_TITLE_LENGTH, PRIORITIES

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
    priority: str = Field(
        PRIORITIES[0], description=f"The task priority. Values={PRIORITIES}"
    )
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
    priority: str | None = PRIORITIES[0]
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
    priority: str | None = PRIORITIES[0]
    last_completed: date | None = None
    repeat_interval: int | None = None
    user_id: int | None = None
    tags: List[TagModel] | None = None


class PriorityUpdate(BaseModel):
    priority: str


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
