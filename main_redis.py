import redis

# Подключение к Redis
r = redis.Redis(host='localhost', port=5672, db=0, decode_responses=True)

try:
    r.ping()
    print("Успешное подключение к Redis")
except redis.ConnectionError:
    print("Ошибка подключения к Redis")