from __future__ import annotations

import pytest
from redis import Redis


@pytest.fixture(scope="session")
def test_fixture_scope(redis_url):
    assert redis_url


@pytest.fixture(scope="session")
def server_id(redis_server):
    return id(redis_server)


def test_redis_url(redis_url, test_fixture_scope):
    assert redis_url
    assert redis_url.startswith("unix://")


def test_redis(redis_url):
    redis = Redis.from_url(redis_url)
    redis.set("foo", "bar")
    assert redis.get("foo") == b"bar"


def test_autoflash(redis_url):
    redis = Redis.from_url(redis_url)
    assert redis.get("foo") is None


def test_server_is_session_scoped(redis_server, server_id):
    assert id(redis_server) == server_id


def test_redis_factory(redis_factory):
    with redis_factory() as rdb:
        rdb.set("factory_key", "factory_value")
        assert rdb.get("factory_key") == b"factory_value"
