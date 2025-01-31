import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB.session import Base

from models.User import User
from services.User import *

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
def test_users(db):
    """Dummy users for testing"""
    user1 = User(name="Michael", email="michael@dundermifflin.com")
    user2 = User(name="Dwight", email="dwight@dundermifflin.com")
    db.add(user1)
    db.add(user2)
    db.commit()
    db.refresh(user1)
    db.refresh(user2)
    return [user1, user2]


def test_get_all_users(test_users, db):
    users = get_all_users(db)
    assert len(users) == 2
    assert users[0].name == "Michael"
    assert users[1].name == "Dwight"


def test_create_user(db):
    user = User(name="Pam", email="pam@dundermifflin.com")
    created_user = create_user(db, user)
    retrieved_user = db.query(User).filter_by(name="Pam").first()
    assert retrieved_user == created_user
