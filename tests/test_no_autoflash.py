from __future__ import annotations

import pytest
from redis import Redis


@pytest.fixture(autouse=True)
def redis_autoflash():
    """Override the plugin fixture to disable auto-flushing."""
    return False


def test_set_persisted_value(redis_url):
    redis = Redis.from_url(redis_url)
    redis.set("persisted", "value")
    assert redis.get("persisted") == b"value"


def test_persisted_value_survives(redis_url):
    redis = Redis.from_url(redis_url)
    assert redis.get("persisted") == b"value"
