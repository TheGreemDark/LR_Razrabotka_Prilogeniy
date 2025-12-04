import redis

r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

try:
    r.ping()
    print("Connected to Redis\n")
    
    # Установка и получение значения
    print("=== Работа со строками ===")
    r.set("user:name", "Иван")
    name = r.get("user:name")
    print(f"Name: {name}")
    
    # Установка с TTL (время жизни)
    print("\n=== Установка с TTL ===")
    r.setex("session:123", 3600, "active")  # 1 час
    print("Session set with 1 hour TTL")
    
    # Работа с числами
    print("\n=== Работа с числами ===")
    r.set("counter", 0)
    r.incr("counter")  # Увеличить на 1
    print(f"Counter after incr: {r.get('counter')}")
    r.incrby("counter", 5)  # Увеличить на 5
    print(f"Counter after incrby(5): {r.get('counter')}")
    r.decr("counter")  # Уменьшить на 1
    print(f"Counter after decr: {r.get('counter')}")
    
    # Добавление элементов в список
    print("\n=== Работа со списками ===")
    r.delete("tasks")  # Очистим список если существует
    r.lpush("tasks", "task1", "task2")  # Добавить в начало
    print(f"Tasks after lpush: {r.lrange('tasks', 0, -1)}")
    
    r.rpush("tasks", "task3", "task4")  # Добавить в конец
    print(f"Tasks after rpush: {r.lrange('tasks', 0, -1)}")
    
    # Получение элементов
    tasks = r.lrange("tasks", 0, -1)  # Все элементы
    print(f"\nAll tasks: {tasks}")
    
    first_task = r.lpop("tasks")  # Удалить и вернуть первый
    print(f"First task (removed): {first_task}")
    
    last_task = r.rpop("tasks")  # Удалить и вернуть последний
    print(f"Last task (removed): {last_task}")
    
    # Получение длины списка
    length = r.llen("tasks")
    print(f"\nRemaining tasks count: {length}")
    print(f"Remaining tasks: {r.lrange('tasks', 0, -1)}")
    
    # Работа с множествами (Sets)
    print("\n=== Работа с множествами ===")
    r.delete("tags", "languages")  # Очистим множества
    r.sadd("tags", "python", "redis", "database")
    r.sadd("languages", "python", "java", "javascript")
    print(f"Tags: {r.smembers('tags')}")
    print(f"Languages: {r.smembers('languages')}")
    
    # Проверка принадлежности
    is_member = r.sismember("tags", "python")
    print(f"\nIs 'python' in tags? {is_member}")
    
    # Получение всех элементов
    all_tags = r.smembers("tags")
    print(f"All tags: {all_tags}")
    
    # Операции с множествами
    intersection = r.sinter("tags", "languages")  # Пересечение
    print(f"\nIntersection (tags ∩ languages): {intersection}")
    
    union = r.sunion("tags", "languages")  # Объединение
    print(f"Union (tags ∪ languages): {union}")
    
    difference = r.sdiff("tags", "languages")  # Разность
    print(f"Difference (tags - languages): {difference}")
    
    # Работа с хэшами (Hash)
    print("\n=== Работа с хэшами ===")
    r.delete("user:1000")  # Очистим хэш
    r.hset("user:1000", mapping={
        "name": "Иван",
        "age": "30",
        "city": "Москва"
    })
    
    # Получение значений
    name = r.hget("user:1000", "name")
    print(f"User name: {name}")
    
    all_data = r.hgetall("user:1000")
    print(f"All user data: {all_data}")
    
    # Проверка существования поля
    exists = r.hexists("user:1000", "email")
    print(f"\nDoes 'email' field exist? {exists}")
    
    # Получение всех ключей или значений
    keys = r.hkeys("user:1000")
    values = r.hvals("user:1000")
    print(f"Keys: {keys}")
    print(f"Values: {values}")
    
    # Работа с упорядоченными множествами (Sorted Sets)
    print("\n=== Работа с упорядоченными множествами ===")
    r.delete("leaderboard")  # Очистим leaderboard
    r.zadd("leaderboard", {
        "player1": 100,
        "player2": 200,
        "player3": 150
    })
    
    # Получение элементов по рангу (от меньшего к большему)
    top_players = r.zrange("leaderboard", 0, 2, withscores=True)
    print(f"Top 3 players (ascending): {top_players}")
    
    # Получение элементов по рангу (от большего к меньшему)
    top_players_desc = r.zrevrange("leaderboard", 0, 2, withscores=True)
    print(f"Top 3 players (descending): {top_players_desc}")
    
    # Получение элементов по оценке
    players_by_score = r.zrangebyscore("leaderboard", 100, 200, withscores=True)
    print(f"\nPlayers with score 100-200: {players_by_score}")
    
    # Получение ранга элемента
    rank = r.zrank("leaderboard", "player1")
    print(f"Rank of player1: {rank}")
    
    # Получение оценки элемента
    score = r.zscore("leaderboard", "player2")
    print(f"Score of player2: {score}")
    
except redis.ConnectionError as e:
    print(f"✗ Failed to connect to Redis: {e}")