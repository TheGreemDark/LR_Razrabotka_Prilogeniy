import requests

def delete_user(user_id: int):
    """Удалить пользователя"""
    response = requests.delete(f"http://127.0.0.1:8000/users/{user_id}")
    
    print(f"\nУдаление пользователя с ID {user_id}:")
    print(f"Статус: {response.status_code}")
    # На успешное удаление сервер может вернуть 200 или 204.
    # В случае 204 тело ответа пустое — не вызывать response.json() без проверки.
    if response.status_code in (200, 204):
        # Попробуем распечатать тело ответа, если оно есть
        text = response.text.strip()
        if text:
            try:
                print("Ответ:", response.json())
            except Exception:
                print("Ответ (raw):", text)
        else:
            print("Ответ: (empty body) - удаление выполнено")
        return

    # Ошибка: попытаемся распечатать JSON-ответ, если он есть, иначе raw text
    try:
        print("Ответ:", response.json())
    except ValueError:
        # Пустой или не-JSON ответ
        print("Ответ (raw):", response.text)

def check_user_exists(user_id: int) -> bool:
    """Проверить существование пользователя"""
    response = requests.get(f"http://127.0.0.1:8000/users/{user_id}")
    return response.status_code == 200

if __name__ == "__main__":
    user_id = 3
    
    # Проверить, существует ли пользователь
    if check_user_exists(user_id):
        # Удалить пользователя
        delete_user(user_id)
        
        # Проверить, что пользователь действительно удален
        if not check_user_exists(user_id):
            print(f"Пользователь с ID {user_id} успешно удален")
    else:
        print(f"Пользователь с ID {user_id} не найден")
    
    # Попытка удалить несуществующего пользователя
    delete_user(999)