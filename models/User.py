from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship, validates

from DB.session import Base
from config import settings


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(settings.MAX_USER_NAME_LENGTH), nullable=False)
    email = Column(String, nullable=False, unique=True)
    active = Column(Boolean, default=True)

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")

    @validates("name")
    def validate_name_length(self, _, value):
        if len(value) > settings.MAX_USER_NAME_LENGTH:
            raise ValueError(
                f"User name cannot exceed {settings.MAX_USER_NAME_LENGTH} characters. Provided: {len(value)}"
            )
        return value
