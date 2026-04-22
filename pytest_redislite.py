from __future__ import annotations

import contextlib
import os
import shutil
import signal
from contextlib import contextmanager
from pathlib import Path

import pytest
from redislite import Redis

__version__ = "0.1.0"


def pytest_addoption(parser):
    parser.addoption(
        "--redis-path", action="store", dest="redis_path", help="Path to Redis Database"
    )
    parser.addini(name="redis_path", help="Path to Redis Database")
    parser.addoption(
        "--redis-socket-path",
        action="store",
        dest="redis_socket",
        help="Path to Redis Socket",
    )
    parser.addini(name="redis_socket_path", help="Path to Redis Socket")


@pytest.fixture(scope="session")
def redis_path(request):
    cfg = request.config
    return cfg.getoption("--redis-path") or cfg.getini("redis_path")


@pytest.fixture(scope="session")
def redis_socket_path(request):
    cfg = request.config
    return cfg.getoption("--redis-socket-path") or cfg.getini("redis_socket_path")


@pytest.fixture(scope="session")
def redis_factory(redis_path, redis_socket_path):
    @contextmanager
    def factory():
        rdb = Redis(redis_path, unix_socket_path=redis_socket_path)
        try:
            yield rdb
        finally:
            pid = getattr(rdb, "pid", None)
            if pid:
                with contextlib.suppress(ProcessLookupError):
                    os.kill(pid, signal.SIGKILL)

            socket_file = getattr(rdb, "socket_file", None)
            if socket_file:
                Path(socket_file).unlink(missing_ok=True)

            redis_dir = getattr(rdb, "redis_dir", None)
            if redis_dir:
                shutil.rmtree(redis_dir, ignore_errors=True)

    return factory


@pytest.fixture(scope="session")
def redis_server(redis_factory):
    with redis_factory() as rdb:
        yield rdb


@pytest.fixture(scope="session")
def redis_url(redis_server):
    return f"unix://{redis_server.socket_file}"


@pytest.fixture(autouse=True)
def redis_autoflash(request, redis_server):
    redis_server.flushall()
