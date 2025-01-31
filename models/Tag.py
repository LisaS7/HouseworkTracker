from sqlalchemy import Table, Column, Integer, String, ForeignKey
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

    @validates("name")
    def validate_name_length(self, _, value):
        if len(value) > settings.MAX_TAG_LENGTH:
            raise ValueError(
                f"Tag name cannot exceed {settings.MAX_TAG_LENGTH} characters. Provided: {len(value)}"
            )
        return value
