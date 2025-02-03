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
    user1 = User(name="Lisa", email="lisa@example.com")
    user2 = User(name="Simon", email="simon@example.com")

    # create_user(db, user1)
    # create_user(db, user2)

    living_room = Tag(name="Living Room")
    kitchen = Tag(name="Kitchen")
    downstairs_hall = Tag(name="Hall (Downstairs)")
    office = Tag(name="Office")
    alec_room = Tag(name="Alec's Room")
    our_room = Tag(name="Our Room")
    shower = Tag(name="Shower")
    bathroom = Tag(name="Bathroom")

    tags = [
        living_room,
        kitchen,
        downstairs_hall,
        office,
        alec_room,
        our_room,
        shower,
        bathroom,
    ]

    # for tag in tags:
    #     create_tag(db, tag)

    tasks = [
        Task(
            title="Mop floor",
            priority=Priority.LOW,
            last_completed="2025-01-21",
            user=user1,
            tags=[kitchen],
        ),
        Task(title="Change bed", user=user1, tags=[our_room]),
        Task(title="Clean toilet", user=user1, tags=[bathroom]),
        Task(title="Clean sink", user=user1, tags=[bathroom]),
        Task(title="Clean worktops", user=user1, tags=[kitchen]),
        Task(title="Empty cardboard recycling", user=user1, tags=[kitchen]),
        Task(title="Clean and tidy dining table", user=user1, tags=[living_room]),
        Task(title="Empty main bin", user=user1, tags=[kitchen]),
        Task(title="Empty plastic/cans recycling", user=user1, tags=[kitchen]),
        Task(title="Clean sink", user=user1, tags=[kitchen]),
    ]

    # for task in tasks:
    #     create_task(db, task)
