import pytest
from datetime import date
from sqlalchemy.exc import IntegrityError

from models.Task import Task, Priority
from models.Tag import Tag
from models.User import User
from config import MAX_TITLE_LENGTH, MAX_TAG_LENGTH, MAX_USER_NAME_LENGTH


# ---------- FIXTURES ----------


@pytest.fixture
def test_user(db):
    """A dummy user for testing"""
    user = User(name="Bob", email="bob@housework.co.uk")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------- TASK ----------


def test_create_task(test_user, db):
    task = Task(title="Mop kitchen", user_id=test_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    retrieved_task = db.query(Task).filter_by(title="Mop kitchen").first()

    assert retrieved_task is not None
    assert retrieved_task.user_id == test_user.id


def test_no_title(test_user, db):
    task = Task(user_id=test_user.id)
    db.add(task)

    with pytest.raises(IntegrityError):
        db.commit()


def test_long_title(test_user):
    max_length = MAX_TITLE_LENGTH
    test_length = max_length + 10
    long_title = "A" * (test_length)

    with pytest.raises(
        ValueError,
        match=f"Title cannot exceed {max_length} characters. Provided: {test_length}",
    ):
        Task(title=long_title, user_id=test_user.id)


def test_default_priority(test_user, db):
    task = Task(title="Test Priority", user_id=test_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    retrieved_task = db.query(Task).filter_by(title="Test Priority").first()

    assert retrieved_task.priority == Priority.LOW


def test_invalid_priority(test_user):
    invalid_word = "Banana"
    with pytest.raises(ValueError, match=f"{invalid_word} is not a valid priority"):
        Task(title="Test Priority", priority=invalid_word, user_id=test_user.id)


def test_last_completed(test_user, db):
    last_date = date(2025, 1, 1)
    task = Task(title="Test Date", user_id=test_user.id, last_completed=last_date)
    db.add(task)
    db.commit()
    db.refresh(task)
    retrieved_task = db.query(Task).filter_by(title="Test Date").first()

    assert retrieved_task.last_completed == last_date


def test_invalid_date(test_user, db):
    test = "Banana"
    with pytest.raises(
        ValueError, match="Date is invalid, you provided Banana of type <class 'str'>"
    ):
        Task(title="Test Date", user_id=test_user.id, last_completed=test)


# ---------- TAGS ----------


def test_task_with_tags(test_user, db):
    task = Task(title="Test Tags", user_id=test_user.id)
    tag1 = Tag(name="Living Room")
    tag2 = Tag(name="Kitchen")
    task.tags = [tag1, tag2]

    db.add(task)
    db.commit()
    db.refresh(task)

    retrieved_task = db.query(Task).filter_by(title="Test Tags").first()

    assert len(retrieved_task.tags) == 2
    assert retrieved_task.tags[0].name == "Living Room"
    assert retrieved_task.tags[1].name == "Kitchen"


def test_long_tag_name(db):
    max_length = MAX_TAG_LENGTH
    test_length = max_length + 10
    long_name = "A" * (test_length)

    with pytest.raises(
        ValueError,
        match=f"Tag name cannot exceed {max_length} characters. Provided: {test_length}",
    ):
        Tag(name=long_name)


# ---------- USER ----------


def test_default_active(db):
    user = User(name="Pam", email="pam@dundermifflin.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    retrieved_user = db.query(User).filter_by(name="Pam").first()

    assert retrieved_user.active == True


def test_unique_email(db):
    user1 = User(name="Michael", email="michael@dundermifflin.com")
    user2 = User(name="Dwight", email="michael@dundermifflin.com")

    db.add(user1)
    db.add(user2)

    with pytest.raises(IntegrityError):
        db.commit()


def test_long_user_name(db):
    max_length = MAX_USER_NAME_LENGTH
    test_length = max_length + 10
    long_name = "A" * (test_length)

    with pytest.raises(
        ValueError,
        match=f"User name cannot exceed {max_length} characters. Provided: {test_length}",
    ):
        User(name=long_name)


# ---------- RELATIONSHIP ----------


def test_get_tasks_for_user(test_user, db):
    task1 = Task(title="Test Task 1", user_id=test_user.id)
    task2 = Task(title="Test Task 2", user_id=test_user.id)
    db.add(task1)
    db.add(task2)
    db.commit()

    tasks = db.query(Task).filter(Task.user_id == test_user.id).all()

    assert len(tasks) == 2
    assert tasks[0].title == "Test Task 1"
    assert tasks[1].title == "Test Task 2"
    assert all(task.user_id == test_user.id for task in tasks)
