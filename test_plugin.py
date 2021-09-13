def test_redis_url(redis_url):
    assert redis_url
    assert redis_url.startswith('unix://')


def test_redis(redis_url):
    from redis import Redis

    redis = Redis.from_url(redis_url)
    redis.set('foo', 'bar')
    assert redis.get('foo') == b'bar'


def test_autoflash(redis_url):
    from redis import Redis

    redis = Redis.from_url(redis_url)
    assert redis.get('foo') is None
