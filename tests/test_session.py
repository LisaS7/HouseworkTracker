import pytest
from DB.session import Database


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
    settings = Database(in_docker, platform)
    assert settings.get_host() == expected_host
