import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError


from DB.Task import Task, Priority, Tag
from DB.User import User
from DB.session import Base
from config import settings


engine = create_engine("sqlite:///:memory:", echo=True)
Session = sessionmaker(bind=engine)


# ---------- FIXTURES ----------


@pytest.fixture
def create_tables():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db(create_tables):
    test_session = Session()
    yield test_session
    test_session.close()


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
    max_length = settings.MAX_TITLE_LENGTH
    test_length = max_length + 10
    long_title = "A" * (test_length)

    with pytest.raises(
        ValueError,
        match=f"Title cannot exceed {max_length} characters. Provided: {test_length}",
    ):
        task = Task(title=long_title, user_id=test_user.id)


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
        task = Task(title="Test Priority", priority=invalid_word, user_id=test_user.id)


def test_due_date(test_user, db):
    due_date = date(2025, 1, 1)
    task = Task(title="Test Date", user_id=test_user.id, due_date=due_date)
    db.add(task)
    db.commit()
    db.refresh(task)
    retrieved_task = db.query(Task).filter_by(title="Test Date").first()

    assert retrieved_task.due_date == due_date


def test_invalid_date(test_user, db):
    due_date = "Banana"
    with pytest.raises(
        ValueError, match="Date is invalid, you provided Banana of type <class 'str'>"
    ):
        task = Task(title="Test Date", user_id=test_user.id, due_date=due_date)


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


# ---------- USER ----------


def test_default_active(db):
    user = User(name="Michael Scott", email="michael@dundermifflin.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    retrieved_user = db.query(User).filter_by(name="Michael Scott").first()

    assert retrieved_user.active == True


def test_unique_email(db):
    user1 = User(name="Michael", email="michael@dundermifflin.com")
    user2 = User(name="Dwight", email="michael@dundermifflin.com")

    db.add(user1)
    db.add(user2)

    with pytest.raises(IntegrityError):
        db.commit()


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
