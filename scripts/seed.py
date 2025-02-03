from models.Task import Task, Priority
from models.Tag import Tag
from models.User import User
from services.User import create_user
from services.Tag import create_tag
from services.Task import create_task
from DB.session import database

local = database.get_session()
db = local()


def seed():
    user1 = User(name="Michael", email="michael@dundermifflin.com")
    user2 = User(name="Dwight", email="dwight@dundermifflin.com")

    # create_user(db, user1)
    # create_user(db, user2)

    tag1 = Tag(name="Tag1")
    tag2 = Tag(name="Tag2")
    create_tag(db, tag1)
    create_tag(db, tag2)

    tasks = [
        Task(
            title="Mop kitchen",
            priority=Priority.HIGH,
            due_date="2025-01-21",
            user=user1,
        ),
        Task(title="Clean oven", due_date="2025-01-30", user=user1),
        Task(title="Wash dishes", due_date="2025-02-15", user=user2),
        Task(title="Feed the cat", due_date="2025-02-04", user=user2),
        Task(
            title="Grocery shopping", due_date="2025-04-30", user=user2, complete=True
        ),
    ]

    tasks[0].tags = [tag1, tag2]
    tasks[1].tags = [tag2]
    tasks[2].tags = [tag1]

    for task in tasks:
        create_task(db, task)
