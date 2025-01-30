from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship

from DB.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    active = Column(Boolean, default=True)

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
