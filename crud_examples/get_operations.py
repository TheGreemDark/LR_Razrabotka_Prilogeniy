import requests

def get_all_users():
    """Получить список всех пользователей"""
    response = requests.get("http://127.0.0.1:8000/users")
    print("\nСписок всех пользователей:")
    print(f"Статус: {response.status_code}")
    print("Данные:", response.json())

def get_user_by_id(user_id: int):
    """Получить пользователя по ID"""
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}")
    print(f"\nПользователь с ID {user_id}:")
    print(f"Статус: {response.status_code}")
    if response.status_code == 200:
        print("Данные:", response.json())
    else:
        print("Ошибка:", response.json())

if __name__ == "__main__":
    # Получить всех пользователей
    get_all_users()
    
    # Получить пользователя с ID=1
    get_user_by_id(1)
    
    # Попробовать получить несуществующего пользователя
    get_user_by_id(999)