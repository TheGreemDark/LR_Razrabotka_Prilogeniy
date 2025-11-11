import requests

def create_user(username: str, email: str, full_name: str = None):
    """Создать нового пользователя"""
    user_data = {
        "username": username,
        "email": email,
        "full_name": full_name
    }
    
    response = requests.post(
        "http://127.0.0.1:8000/users",
        json=user_data
    )
    
    print(f"\nСоздание пользователя {username}:")
    print(f"Статус: {response.status_code}")
    print("Ответ:", response.json())
    return response.json() if response.status_code == 200 else None

if __name__ == "__main__":
    # Создать нового пользователя
    create_user(
        username="Loken_X",
        email="Loken_X_Istvaan_III@example.com",
        full_name="Локен Хорусович"
    )
    
    # Попытка создать пользователя с тем же именем (должна вернуть ошибку)
    create_user(
         username="Loken_X",
        email="Loken_X_Istvaan_III@example.com",
        full_name="Локен Хорусович"
    )