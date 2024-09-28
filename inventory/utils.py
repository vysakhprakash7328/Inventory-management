import logging
import redis
from django.conf import settings

def get_logger(name='inventory'):
    """Get a logger instance for the specified name."""
    return logging.getLogger(name)

redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)

def get_cache(key):
    """Retrieve value from cache by key."""
    return redis_client.get(key)

def set_cache(key, value, timeout):
    """Set value in cache with a timeout."""
    redis_client.setex(key, timeout, value)
