import logging
import random
from typing import Callable

import pytest
from fastapi.testclient import TestClient

from ._fixtures.servers import UvicornTestServerProcess, UvicornTestServerThread
from ._fixtures.utils import UniqueRandomStringFactory, get_unused_tcp_port


def pytest_addoption(parser):
    parser.addoption("--server-port", action="store", type=int)
    parser.addoption("--server-host", action="store", type=int)


def pytest_generate_tests(metafunc):
    if "server_port" in metafunc.fixturenames:
        metafunc.parametrize("server_port", [metafunc.config.getoption("server_port")])
        metafunc.parametrize("server_host", [metafunc.config.getoption("server_host")])


@pytest.mark.skip
@pytest.fixture(autouse=True)
def suppress_application_log_capture(caplog):
    caplog.set_level(logging.CRITICAL, logger="")
    caplog.set_level(logging.CRITICAL, logger="live")


@pytest.fixture
def app():
    from app.main import app

    yield app


@pytest.fixture
def client(app):
    """Make a 'client' fixture available to test cases."""
    # Creating within a context manager ensures that and shutdown with every test case.
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def server_thread_factory(app):
    server_threads = []

    def _server_thread_factory(*args, **kwargs):
        nonlocal server_threads
        server_thread = UvicornTestServerThread(app=app, port=get_unused_tcp_port())
        server_thread(*args, **kwargs)
        server_threads.append(server_thread)
        return server_thread

    yield _server_thread_factory

    for server_thread in server_threads:
        server_thread.stop()


@pytest.fixture
def server_thread(server_thread_factory):
    yield server_thread_factory()


@pytest.fixture
def server_proc(xprocess, request):
    yield UvicornTestServerProcess(
        xprocess_instance=xprocess,
        app="app.main:app",
        host="127.0.0.1",
        port=get_unused_tcp_port(),
        env={
            "PYTHONPATH": request.config.rootdir,
            "SECRET_KEY": "not_secret_test_key",
            "ALLOWED_HOSTS": "localhost,127.0.0.1",
            "DATABASE_URL": "sqlite:///db.sqlite3",
            "REDIS_URL": "redis://localhost:6379",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
    )


@pytest.fixture
def random_string_factory() -> Callable:
    return UniqueRandomStringFactory()


@pytest.fixture
def guest_name_factory() -> Callable:
    """Create a new random guest name"""

    def _guest_name_factory():
        return UniqueRandomStringFactory(
            letters=True,
            numbers=False,
            num_words_min=1,
            num_words_max=3,
            word_length_min=3,
            word_length_max=9,
        ).title()

    return _guest_name_factory


@pytest.fixture
def feature_title_factory() -> Callable:
    return UniqueRandomStringFactory(
        letters=True,
        numbers=False,
        num_words_min=2,
        num_words_max=3,
        word_length_min=2,
        word_length_max=9,
    )


@pytest.fixture
def session_key_factory() -> Callable[[], str]:
    """Create a new random 32-character integer that imitates a session key"""
    return UniqueRandomStringFactory(
        letters=True,
        numbers=True,
        num_words_min=1,
        num_words_max=1,
        word_length_min=32,
        word_length_max=32,
    )


@pytest.fixture
def random_euler_rotation():
    return [random.uniform(0, 360) for i in range(3)]
