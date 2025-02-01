import pytest
from DB.session import Base

from models.Task import Task, Priority
from models.User import User
from models.Tag import Tag
from services.Task import *

from datetime import date
from tests.conftest import engine, session

TODAY = date.today()


@pytest.fixture
def create_tables():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db(create_tables):
    test_session = session()
    yield test_session
    test_session.close()


@pytest.fixture
def test_users(db):
    """Dummy users for testing"""
    user1 = User(name="Michael", email="michael@dundermifflin.com")
    user2 = User(name="Dwight", email="dwight@dundermifflin.com")
    db.add_all([user1, user2])
    db.commit()
    db.refresh(user1)
    db.refresh(user2)
    return [user1, user2]


@pytest.fixture
def test_tasks(test_users, db):
    """Dummy tasks for testing"""
    user1, user2 = test_users

    tasks = [
        Task(
            title="Mop kitchen",
            priority=Priority.HIGH,
            due_date="2025-01-21",
            user=user1,
        ),
        Task(title="Clean oven", due_date="2025-01-30", user=user1),
        Task(title="Wash dishes", due_date=TODAY, user=user2),
        Task(title="Feed the cat", due_date=date.today(), user=user2),
        Task(
            title="Grocery shopping", due_date="2025-04-30", user=user2, complete=True
        ),
    ]

    db.add_all(tasks)
    db.commit()

    for task in tasks:
        db.refresh(task)

    return tasks


@pytest.fixture
def test_tags(db):
    """Dummy tags for testing"""
    tag1 = Tag(name="Tag1")
    tag2 = Tag(name="Tag2")
    db.add_all([tag1, tag2])
    db.commit()
    db.refresh(tag1)
    db.refresh(tag2)
    return [tag1, tag2]


def test_get_all_tasks(test_tasks, db):
    tasks = get_all_tasks(db)
    assert len(tasks) == 5
    assert tasks[0].title == "Mop kitchen"


def test_get_all_incomplete_tasks(test_tasks, db):
    tasks = get_all_incomplete_tasks(db)
    assert len(tasks) == 4
    for task in tasks:
        assert not task.complete


def test_get_overdue_tasks(test_tasks, db):
    tasks = get_all_overdue_tasks(db)
    assert len(tasks) == 2
    for task in tasks:
        assert task.due_date < date.today()


def test_get_today_tasks(test_tasks, db):
    tasks = get_todays_tasks(db)
    assert len(tasks) == 2
    for task in tasks:
        assert task.due_date == TODAY


def test_get_tasks_by_user(test_tasks, db):
    tasks = get_tasks_by_user(db, 1)
    assert len(tasks) == 2
    for task in tasks:
        assert task.user_id == 1


def test_get_task_by_id(test_tasks, db):
    task = get_task_by_id(db, 3)
    assert task.title == "Wash dishes"


def test_task_not_found(test_tasks, db):
    with pytest.raises(TaskNotFoundException, match="Task not found for id 23"):
        task = get_task_by_id(db, 23)


def test_create_task(test_users, db):
    user = test_users[0]
    task = Task(title="Buy cheese", due_date="2025-01-30", user=user)
    created_task = create_task(db, task)
    retrieved_task = db.query(Task).filter_by(title="Buy cheese").first()
    assert retrieved_task == created_task


def test_update_task(test_tasks, db):
    update_task(db, 1, {"title": "Laundry"})
    retrieved_task = db.query(Task).filter(Task.id == 1).first()
    assert retrieved_task.title == "Laundry"
    assert retrieved_task.due_date == date(2025, 1, 21)


def test_delete_task(test_tasks, db):
    delete_task(db, 2)
    tasks = db.query(Task).all()
    deleted_task = db.query(Task).filter(Task.id == 2).first()
    assert len(tasks) == 4
    assert not deleted_task


def test_add_tags_to_task(test_tasks, test_tags, db):
    add_tags_to_task(db, test_tasks[0], test_tags)
    retrieved_task = db.query(Task).filter(Task.id == 1).first()
    assert retrieved_task.tags == test_tags


def test_get_tags_by_task(test_tasks, db):
    tags = [Tag(name="Tag1"), Tag(name="Tag2")]
    test_tasks[0].tags = tags
    retrieved_tags = get_tags_by_task(db, 1)
    assert retrieved_tags == tags


def test_get_tasks_by_tag(test_tasks, test_tags, db):
    test_tasks[0].tags = test_tags
    test_tasks[1].tags = test_tags
    retrieved_tasks = get_tasks_by_tag(db, test_tags[0])
    assert retrieved_tasks == [test_tasks[0], test_tasks[1]]


def test_get_no_tags(test_tasks, db):
    tags = get_tags_by_task(db, 1)
    assert tags == None


def test_remove_tag_from_task(test_tasks, test_tags, db):
    task = test_tasks[0]
    tag_to_remove = test_tags[0]
    task.tags = test_tags

    updated_task = remove_tag_from_task(db, 1, tag_to_remove)
    retrieved_task = db.query(Task).filter(Task.id == 1).first()

    assert updated_task == retrieved_task
    assert len(retrieved_task.tags) == 1
    assert tag_to_remove not in retrieved_task.tags
