import datetime as dt
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Computed
from sqlalchemy.orm import relationship, validates

from models.Tag import task_tags
from DB.session import Database
from config import logger, MAX_TITLE_LENGTH, TESTING, PRIORITIES

if TESTING:
    next_due_query = "DATE(last_completed, '+' || repeat_interval || ' day')"
else:
    next_due_query = "last_completed + repeat_interval * interval '1 day'"


class Task(Database.Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(MAX_TITLE_LENGTH), nullable=False)
    priority = Column(String, default="LOW")
    last_completed = Column(Date)
    repeat_interval = Column(Integer, default=0)

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

    @validates("repeat_interval")
    def validate_repeat_interval(self, _, value):
        if not isinstance(value, int):
            try:
                int_value = int(value)
            except:
                message = f"{value} is not a valid integer"
                logger.error(message)
                raise ValueError(message)

        if int_value > 0:
            return int_value
        else:
            message = f"Repeat interval cannot be a negative number ({value})"
            logger.error(message)
            raise ValueError(message)

    @validates("priority")
    def validate_priority(self, _, value):
        if value not in PRIORITIES:
            message = f"{value} is not a valid priority"
            logger.error(f"ValueError: {message}")
            raise ValueError(message)
        else:
            return value

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
        return f"<Task id={self.id} title={self.title} priority={self.priority} last_completed={self.last_completed} repeat_interval={self.repeat_interval} user_id={self.user_id} tag_count={len(self.tags)}>"
