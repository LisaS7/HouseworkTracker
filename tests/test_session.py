import pytest
from DB.session import get_engine
from config import Settings


def test_engine_creation():
    engine, _ = get_engine(testing=True)
    assert str(engine.url) == "sqlite:///:memory:"

    engine, _ = get_engine(testing=False)
    assert str(engine.url).startswith("postgresql")


@pytest.mark.parametrize(
    "in_docker, platform, expected_host",
    [
        (True, "linux", "172.17.0.1"),
        (True, "win32", "host.docker.internal"),
        (False, "linux", "localhost"),
        (False, "macos", "localhost"),
    ],
)
def test_host(in_docker, platform, expected_host):
    settings = Settings(in_docker, platform)
    assert settings.get_host() == expected_host
