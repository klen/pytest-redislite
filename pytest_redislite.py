import pytest


__version__ = '0.0.3'


def pytest_addoption(parser):
    parser.addoption(
        '--redis-path', action='store', dest='redis_path', help='Path to Redis Database')
    parser.addini(name='redis_path', help='Path to Redis Database')
    parser.addoption(
        '--redis-socket-path', action='store', dest='redis_socket', help='Path to Redis Socket')
    parser.addini(name='redis_socket_path', help='Path to Redis Socket')


@pytest.fixture(scope='session')
def redis_path(request):
    cfg = request.config
    return cfg.getoption('--redis-path') or cfg.getini('redis_path')


@pytest.fixture(scope='session')
def redis_socket_path(request):
    cfg = request.config
    return cfg.getoption('--redis-socket-path') or cfg.getini('redis_socket_path')


@pytest.fixture(scope='session')
def redis_factory(redis_path, redis_socket_path):
    from contextlib import contextmanager
    from redislite import Redis

    @contextmanager
    def factory():
        rdb = Redis(redis_path, unix_socket_path=redis_socket_path)
        yield rdb
        rdb.shutdown()

    return factory


@pytest.fixture(scope='session')
def redis_server(redis_factory):
    with redis_factory() as rdb:
        yield rdb


@pytest.fixture
def redis_url(redis_server):
    return f"unix://{redis_server.socket_file}"


@pytest.fixture(autouse=True)
def redis_autoflash(request, redis_server):
    redis_server.flushall()
