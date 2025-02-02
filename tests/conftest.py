import pytest
from DB.session import Database
from models.User import User

database = Database()
database.set_engine(testing=True)


@pytest.fixture(scope="function")
def create_tables():
    Database.Base.metadata.create_all(bind=database.engine)
    yield
    Database.Base.metadata.drop_all(database.engine)


@pytest.fixture(scope="function")
def db(create_tables):
    test_session_local = database.get_session()
    db = test_session_local()
    yield db
    db.close()


# ---------- DATA ----------


@pytest.fixture(scope="function")
def test_users(db):
    """Dummy users for testing"""
    user1 = User(name="Michael", email="michael@dundermifflin.com")
    user2 = User(name="Dwight", email="dwight@dundermifflin.com")
    db.add_all([user1, user2])
    db.commit()
    db.refresh(user1)
    db.refresh(user2)
    return [user1, user2]
