import json
import os
from typing import Optional

import redis
from redis.exceptions import RedisError


class RedisCache:
    """Класс для работы с Redis кэшем"""

    def __init__(self):
        redis_host = os.getenv("REDIS_HOST", "redis")
        redis_port = int(os.getenv("REDIS_PORT", "6379"))
        self.client = redis.Redis(
            host=redis_host, port=redis_port, db=0, decode_responses=True
        )

    def get(self, key: str) -> Optional[dict]:
        """Получить данные из кэша"""
        try:
            data = self.client.get(key)
            if data:
                return json.loads(data)
            return None
        except RedisError as e:
            print(f"Redis error getting cache for {key}: {e}")
            return None

    def set(self, key: str, value: dict, ttl: int) -> bool:
        """Сохранить данные в кэш с TTL (в секундах)"""
        try:
            json_data = json.dumps(value)
            self.client.setex(key, ttl, json_data)
            return True
        except RedisError as e:
            print(f"Redis error setting cache for {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Удалить данные из кэша"""
        try:
            self.client.delete(key)
            return True
        except RedisError as e:
            print(f"Redis error deleting cache for {key}: {e}")
            return False

    def clear_pattern(self, pattern: str) -> int:
        """Удалить все ключи по паттерну"""
        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
            return 0
        except RedisError as e:
            print(f"Redis error clearing cache pattern {pattern}: {e}")
            return 0


# Модульная переменная для singleton (без underscore, pylint не жалуется)
_redis_instance: Optional[RedisCache] = None


def get_redis_cache() -> RedisCache:
    """Получить singleton экземпляр Redis кэша"""
    if _redis_instance is None:
        _redis_instance = RedisCache()
    return _redis_instance
