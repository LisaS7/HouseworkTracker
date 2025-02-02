from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from DB.session import Database
from config import logger, MAX_TAG_LENGTH

# Association Table, Tag -> Task
task_tags = Table(
    "task_tags",
    Database.Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Tag(Database.Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(MAX_TAG_LENGTH), nullable=False)
    tasks = relationship("Task", secondary=task_tags, back_populates="tags")

    @validates("name")
    def validate_name_length(self, _, value):
        message = f"Tag name cannot exceed {MAX_TAG_LENGTH} characters. Provided: {len(value)}"
        if len(value) > MAX_TAG_LENGTH:
            logger.error(f"ValueError: {message}")
            raise ValueError(message)
        return value

    def __str__(self):
        return f"<Tag id={self.id} name={self.name} task_count={len(self.tasks)}>"
