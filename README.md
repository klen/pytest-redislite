# pytest-redislite

**pytest-redislite** -- Is a simple [pytest](https://docs.pytest.org) plugin to
help you test your projects using [Redis](https://redis.io).

[![Tests Status](https://github.com/klen/pytest-redislite/workflows/tests/badge.svg)](https://github.com/klen/pytest-redislite/actions)
[![PYPI Version](https://img.shields.io/pypi/v/pytest-redislite)](https://pypi.org/project/pytest-redislite)
[![Python Versions](https://img.shields.io/pypi/pyversions/pytest-redislite)](https://pypi.org/project/pytest-redislite)

## Features

- Automatically starts/ends Redis for your tests using
  [Redislite](https://github.com/yahoo/redislite)
- Flash Redis Database between tests automatically

## Requirements

- python >= 3.7

## Installation

**pytest-redislite** should be installed using pip: ::

    pip install pytest-redislite

## Usage

When installed the plugin provides the fixture: `redis_url`

```python

    def test_code_with_redis(redis_url):
        from redis import Redis

        redis_client = Redis.from_url(redis_url)
        redis_client.set('key', 'value')
        assert redis_client.get('key', 'value')

```

When you are using the fixture Redis server will be started and finished after
your tests.

## Configuration

The plugins support pytest command line options:

- `--redis-path`: Specify a path to Redis Database file
- `--redis-socket-path`: Specify a path to Redis Socket

as well as pytest `ini` options:

- `redis_path`: Specify a path to Redis Database file
- `redis_socket_path`: Specify a path to Redis Socket


## Auto flush data between tests

By default the plugin erases all data in Redis between tests. If you would like
to change the behaviour define the fixture:

```python

    @pytest.fixture
    def redis_autoflash():
        return False

```

You may define it for a module or whole tests session.

## Bug tracker

If you have any suggestions, bug reports or annoyances please report them to
the issue tracker at https://github.com/klen/pytest-redislite/issues


## Contributing

Development of the project happens at: https://github.com/klen/pytest-redislite


## License

Licensed under a [MIT License](http://opensource.org/licenses/MIT)
