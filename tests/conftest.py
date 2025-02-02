import pytest
from DB.session import Database

database = Database()
database.set_engine(testing=True)


@pytest.fixture
def create_tables(scope="session"):
    Database.Base.metadata.create_all(bind=database.engine)
    yield
    Database.Base.metadata.drop_all(database.engine)


@pytest.fixture
def db(create_tables, scope="function"):
    test_session = database.get_session()
    yield test_session
    test_session.close()
