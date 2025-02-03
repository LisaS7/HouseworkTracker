import enum
import datetime as dt
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, Computed
from sqlalchemy.orm import relationship, validates

from models.Tag import task_tags
from DB.session import Database
from config import logger, MAX_TITLE_LENGTH, TESTING

if TESTING:
    next_due_query = "DATE(last_completed, '+' || repeat_interval || ' day')"
else:
    next_due_query = "last_completed + repeat_interval * interval '1 day'"


class Priority(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Task(Database.Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(MAX_TITLE_LENGTH), nullable=False)
    priority = Column(Enum(Priority), default=Priority.LOW)
    last_completed = Column(Date)
    repeat_interval = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="tasks")

    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")

    next_due = Column(
        Date,
        Computed(next_due_query, persisted=True),
    )

    @validates("title")
    def validate_title_length(self, _, value):
        if len(value) > MAX_TITLE_LENGTH:
            message = f"Title cannot exceed {MAX_TITLE_LENGTH} characters. Provided: {len(value)}"
            logger.error(f"ValueError: {message}")
            raise ValueError(message)
        return value

    @validates("priority")
    def validate_priority(self, _, value):
        if value not in Priority:
            message = f"{value} is not a valid priority"
            logger.error(f"ValueError: {message}")
            raise ValueError(message)

    @validates("last_completed")
    def validate_last_completed_date(self, _, value):
        if isinstance(value, str):
            try:
                return dt.datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                message = f"Date is invalid, you provided {value} of type {type(value)}"
                logger.error(f"ValueError: {message}")
                raise ValueError(message)

        if isinstance(value, dt.date):
            return value

    def __str__(self):
        return f"<Task id={self.id} title={self.title} priority={self.priority} last_completed={self.last_completed} repeat interval={self.repeat_interval} user_id={self.user_id} tag_count={len(self.tags)}>"
