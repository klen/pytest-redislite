# pytest-redislite

**pytest-redislite** — a simple [pytest](https://docs.pytest.org) plugin to help you test your
projects using [Redis](https://redis.io).

[![Tests Status](https://github.com/klen/pytest-redislite/workflows/tests/badge.svg)](https://github.com/klen/pytest-redislite/actions)
[![PYPI Version](https://img.shields.io/pypi/v/pytest-redislite)](https://pypi.org/project/pytest-redislite)
[![Python Versions](https://img.shields.io/pypi/pyversions/pytest-redislite)](https://pypi.org/project/pytest-redislite)

## Features

- Automatically starts/ends Redis
  for your tests using [Redislite](https://github.com/yahoo/redislite)
- Flushes Redis database between tests automatically
- Fast fixture teardown (bypasses slow redislite graceful shutdown)

## Requirements

- Python >= 3.10

## Installation

```bash
pip install pytest-redislite
```

## Usage

When installed, the plugin provides the `redis_url` fixture:

```python
def test_code_with_redis(redis_url):
    from redis import Redis

    redis_client = Redis.from_url(redis_url)
    redis_client.set("key", "value")
    assert redis_client.get("key") == b"value"
```

The Redis server is started once per test session and cleaned up automatically
after all tests finish.

You can also use `redis_url` in your own fixtures to set up Redis-backed integrations
(for example, a cache client or task queue broker):

```python
import pytest
from redis import Redis

@pytest.fixture(scope="session")
def cache(redis_url):
    client = Redis.from_url(redis_url, decode_responses=True)
    yield client
    client.close()

def test_cache_set_and_get(cache):
    cache.set("key", "value")
    assert cache.get("key") == "value"
```

## Configuration

The plugin supports pytest command-line options:

- `--redis-path`: Path to the Redis database file
- `--redis-socket-path`: Path to the Redis Unix socket

And equivalent `pytest.ini` / `pyproject.toml` options:

- `redis_path`
- `redis_socket_path`

## Fixtures

| Fixture | Scope | Description |
|---------|-------|-------------|
| `redis_server` | session | `redislite.Redis` instance managing the server lifecycle |
| `redis_url` | session | Unix socket URL for connecting to the running server |
| `redis_factory` | session | Context manager to manually start/shutdown a redislite server |

## Auto-flush data between tests

By default, the plugin erases all Redis data between tests.
To disable this, override the `redis_autoflash` fixture:

```python
import pytest

@pytest.fixture
def redis_autoflash():
    return False
```

You can scope this override to a module or the entire test session.

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and builds.

```bash
# Install dependencies
uv sync --group dev

# Run tests
uv run pytest tests.py

# Run all tests (including no-autoflash scenario)
uv run pytest tests.py tests_no_autoflash.py

# Build and publish
uv build
uv publish
```

## Bug tracker

If you have any suggestions, bug reports,
or annoyances please report them to the issue tracker at https:
//github.com/klen/pytest-redislite/issues

## Contributing

Development of the project happens at: <https://github.com/klen/pytest-redislite>

## License

Licensed under a [MIT License](http://opensource.org/licenses/MIT)
