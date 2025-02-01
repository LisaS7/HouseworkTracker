import pytest
from DB.session import Base, Database

database = Database()

engine, session = database.get_engine(testing=True)


@pytest.fixture
def create_tables(scope="session"):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db(create_tables, scope="session"):
    test_session = session()
    yield test_session
    test_session.close()
