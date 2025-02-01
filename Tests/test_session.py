from DB.session import get_engine


def test_engine_creation():
    engine, _ = get_engine(testing=True)
    assert str(engine.url) == "sqlite:///:memory:"

    engine, _ = get_engine(testing=False)
    assert str(engine.url).startswith("postgresql")
