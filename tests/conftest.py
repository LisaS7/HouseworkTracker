import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB.session import Base

engine = create_engine("sqlite:///:memory:", echo=False)
Session = sessionmaker(bind=engine)


@pytest.fixture
def create_tables(scope="session"):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db(create_tables, scope="session"):
    test_session = Session()
    yield test_session
    test_session.close()
