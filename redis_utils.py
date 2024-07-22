import redis
import logging
from config import REDIS_HOST, REDIS_PORT


def init_redis():
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        r.ping()  # Проверка подключения
        return r
    except redis.ConnectionError as e:
        logging.error(f"Redis connection error: {e}")
        raise SystemExit("Redis connection error. Please check the Redis server.")
