import json
import os
from typing import Any, Optional

import redis


class RedisCache:
    """Класс для работы с Redis кэшем"""

    def __init__(self):
        redis_host = os.getenv("REDIS_HOST", "redis")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
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
        except Exception as e:
            print(f"Error getting cache for {key}: {e}")
            return None

    def set(self, key: str, value: dict, ttl: int) -> bool:
        """Сохранить данные в кэш с TTL (в секундах)"""
        try:
            json_data = json.dumps(value)
            self.client.setex(key, ttl, json_data)
            return True
        except Exception as e:
            print(f"Error setting cache for {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Удалить данные из кэша"""
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            print(f"Error deleting cache for {key}: {e}")
            return False

    def clear_pattern(self, pattern: str) -> int:
        """Удалить все ключи по паттерну"""
        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Error clearing cache pattern {pattern}: {e}")
            return 0


# Singleton instance
_redis_cache: Optional[RedisCache] = None


def get_redis_cache() -> RedisCache:
    """Получить singleton экземпляр Redis кэша"""
    global _redis_cache
    if _redis_cache is None:
        _redis_cache = RedisCache()
    return _redis_cache
