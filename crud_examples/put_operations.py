import requests
from typing import Optional, Dict, Any

def update_user(user_id: int, **update_data) -> Optional[Dict[str, Any]]:
    """Обновить данные пользователя"""
    # Удаляем None значения из update_data
    update_data = {k: v for k, v in update_data.items() if v is not None}
    
    response = requests.put(
        f"http://127.0.0.1:8000/users/{user_id}",
        json=update_data
    )
    
    print(f"\nОбновление пользователя с ID {user_id}:")
    print(f"Статус: {response.status_code}")
    result = response.json()
    print("Ответ:", result)
    
    if response.status_code == 200:
        print("Пользователь успешно обновлен")
        return result
    elif response.status_code == 404:
        print(f"Пользователь с ID {user_id} не найден")
        return None
    else:
        print(f"Ошибка при обновлении пользователя: {result.get('detail', 'Неизвестная ошибка')}")
        return None

if __name__ == "__main__":
    # Проверяем существующего пользователя (например, с ID=1)
    response = requests.get("http://127.0.0.1:8000/users/1")
    if response.status_code == 200:
        user_id = 4
    else:
        # Если пользователь с ID=1 не найден, попробуем получить список всех пользователей
        response = requests.get("http://127.0.0.1:8000/users")
        users = response.json()
        if users:
            user_id = users[0]['id']  # Берем ID первого пользователя
        else:
            print("Нет доступных пользователей для обновления")
            exit(1)

    # Обновить существующего пользователя
    print("\nПолное обновление пользователя:")
    update_user(
        user_id=user_id,
        username="Cerberus_updated",
        email="Cerberus.new_Out@example.com",
        full_name="Церберус Новый как с завода"
    )
    
    # Частичное обновление (только имя)
    print("\nЧастичное обновление пользователя (только full_name):")
    update_user(
        user_id=user_id,
        full_name="Церберус вновь обновленный"
    )
    
    # Попытка обновить несуществующего пользователя
    print("\nПопытка обновить несуществующего пользователя:")
    update_user(
        user_id=999,
        username="not_exist_someone",
        email="not_someone.exists@example.com"
    )