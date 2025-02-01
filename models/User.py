from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship, validates

from DB.session import Base
from config import logger, MAX_USER_NAME_LENGTH


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(MAX_USER_NAME_LENGTH), nullable=False)
    email = Column(String, nullable=False, unique=True)
    active = Column(Boolean, default=True)

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")

    @validates("name")
    def validate_name_length(self, _, value):
        if len(value) > MAX_USER_NAME_LENGTH:
            message = f"User name cannot exceed {MAX_USER_NAME_LENGTH} characters. Provided: {len(value)}"
            logger.error(f"ValueError: {message}")
            raise ValueError(message)
        return value

    def __str__(self):
        return f"<User id={self.id} name={self.name} email={self.email} active={self.active} task_count={len(self.tasks)}>"
