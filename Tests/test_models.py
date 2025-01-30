import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from DB.Task import Task
from DB.User import User
from DB.session import Base


engine = create_engine("sqlite:///:memory:", echo=True)
Session = sessionmaker(bind=engine)


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


def test_create_task(test_user, db):
    task = Task(title="Mop kitchen", user_id=test_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    retrieved_task = db.query(Task).filter_by(title="Mop kitchen").first()

    assert retrieved_task is not None
    assert retrieved_task.user_id == test_user.id
