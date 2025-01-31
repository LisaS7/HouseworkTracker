import enum
import datetime as dt
from sqlalchemy import Table, Column, Integer, String, Boolean, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship, validates

from DB.session import Base
from config import settings

# Association Table, Tag -> Task
task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(settings.MAX_TAG_LENGTH), nullable=False)
    tasks = relationship("Task", secondary=task_tags, back_populates="tags")


class Priority(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(settings.MAX_TITLE_LENGTH), nullable=False)
    priority = Column(Enum(Priority), default=Priority.LOW)
    due_date = Column(Date)
    complete = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="tasks")

    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")

    @validates("title")
    def validate_title_length(self, _, value):
        if len(value) > settings.MAX_TITLE_LENGTH:
            raise ValueError(
                f"Title cannot exceed {settings.MAX_TITLE_LENGTH} characters. Provided: {len(value)}"
            )
        return value

    @validates("priority")
    def validate_priority(self, _, value):
        if value not in Priority:
            raise ValueError(f"{value} is not a valid priority")

    @validates("due_date")
    def validate_due_date(self, _, value):
        if isinstance(value, str):
            try:
                return dt.datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(
                    f"Date is invalid, you provided {value} of type {type(value)}"
                )

        if isinstance(value, dt.date):
            return value
