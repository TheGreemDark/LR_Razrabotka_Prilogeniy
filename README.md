## Основные команды для запуска

Если терминал ругается, то использовать команду:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

1. Создание и активация виртуального окружения:
```bash
python -m venv venv
```
```bash
.\venv\Scripts\activate  # для Windows
```
```bash
source venv/bin/activate # для Linux/Mac
```

2. Установка зависимостей с помощью импорта файла:
```bash
pip install -r requirements.txt
```

3. Инициализация базы данных:
```bash
python init_db.py
```

4. Запуск самого приложения:
```bash
python -m app.main
```

Сервер запустится по следующему адресу `http://127.0.0.1:8000`, так как когда запускал `http://0.0.0.0:8000`, то ничего не работало.

## Проверка работы docker
1. Построить образ:
```bash
docker compose build
```
docker compose build
2. Запустить сервисы:
```bash
docker compose up
```
docker compose up
3. Построить образ и запустить сервисы:
```bash
docker compose up --build
```
## Проверка работы тестов

В папке `tests` находятся тесты.
Примеры вызовов этих тестов приведены ниже ниже.

### Запуск всех тестов:
```bash
.\venv\Scripts\python.exe -m pytest -v
```

### Запуск тестов по категориям:
```bash
# Тесты репозиториев
.\venv\Scripts\python.exe -m pytest tests/test_user_repository.py -v
.\venv\Scripts\python.exe -m pytest tests/test_order_repository.py -v

# Тесты эндпоинтов
.\venv\Scripts\python.exe -m pytest tests/test_user_api.py -v

# Тест пагинации
.\venv\Scripts\python.exe -m pytest tests/test_product.py -v
```
```bash
# Тесты mock
.\venv\Scripts\python.exe -m pytest tests/test_oprder_service_insufficient_stock.py -v
.\venv\Scripts\python.exe -m pytest tests/test_order_service.py -v
.\venv\Scripts\python.exe -m pytest tests/test_product_service.py -v
.\venv\Scripts\python.exe -m pytest tests/test_user_service.py -v
```
### Запуск конкретного теста:
```bash
# Пример: тест создания пользователя
.\venv\Scripts\python.exe -m pytest tests/test_user_repository.py::TestUserRepository::test_create_user -v

<<<<<<< HEAD
Каждый файл содержит подробные комментарии и примеры использования.
Перед запуском примеров необходимо проверить, что:
1. Сервер запущен (`python -m app.main`)
2. База данных инициализирована (`python init_db.py`)
3. Установлен пакет requests (`pip install requests`)
=======
# Пример: тест эндпоинта GET
.\venv\Scripts\python.exe -m pytest tests/test_user_api.py::test_get_user_by_id_success -v
```
остальные аналогично
>>>>>>> 72ce716fd979f9c6b6c95e7ad66d05746544f8ff

### Запуск с дополнительной информацией:
```bash
# С выводом print-statements
.\venv\Scripts\python.exe -m pytest tests/test_user_repository.py -v -s

# С подробным выводом ошибок
.\venv\Scripts\python.exe -m pytest tests/test_user_repository.py -v --tb=long

# Остановить выполнение при первой ошибке
.\venv\Scripts\python.exe -m pytest -v -x
```

**Доступные тесты:**
- test_order_service_insufficient_stock.py - MOCK тесты для заказов с недостаточным количеством товаров
- test_order_repository.py - тесты репозитория заказов
- test_order_service.py - MOCK тесты для проверки успешности создания заказов
- test_product_service.py - MOCK тесты для продуктов
- test_product.py - пагинация товаров
- test_user_api.py - тесты HTTP эндпоинтов (GET, POST, PUT, DELETE)
- test_user_repository.py - тесты репозитория пользователей
- test_user_service.py - MOCK тесты для пользователей
## API Endpoints (Конечные точки API)

API Endpoints - это URL-адреса, по которым можно выполнять различные операции с данными. В нашем приложении доступны следующие endpoints.

### 1. Получение списка пользователей
- Метод: `GET`
- URL: `http://127.0.0.1:8000/users`
- Описание: Возвращает список всех пользователей
- Как использовать: Просто откройте URL в браузере или выполните GET-запрос

### 2. Получение конкретного пользователя
- Метод: `GET`
- URL: `http://127.0.0.1:8000/users/{user_id}`
- Описание: Возвращает информацию о пользователе по его ID
- Пример: `http://127.0.0.1:8000/users/1` - получить пользователя с ID=1

### 3. Создание нового пользователя
- Метод: `POST`
- URL: `http://127.0.0.1:8000/users`
- Тело запроса (пример):
```json
{
    "username": "Loken_X",
    "email": "Loken_X_Istvaan_III@example.com",
    "first_name": "Локен",
    "last_name": "Хорусович"
}
```
- Как использовать: Отправьте POST-запрос с JSON-данными (можно использовать Postman или curl)

### 4. Обновление пользователя
- Метод: `PUT`
- URL: `http://127.0.0.1:8000/users/{user_id}`
- Тело запроса (пример):
```json
{
    "first_name": "Церберус",
    "last_name": "Нехорусович"
}
```
- Примечание: Все поля опциональны, можно обновить только нужные поля

### 5. Удаление пользователя
- Метод: `DELETE`
- URL: `http://127.0.0.1:8000/users/{user_id}`
- Описание: Удаляет пользователя с указанным ID
- Как использовать: Отправьте DELETE-запрос на URL с ID пользователя
## Модели данных

### User (Пользователь)
- `id` - уникальный идентификатор
- `username` - имя пользователя (уникальное)
- `email` - email (уникальный)
- `first_name` - имя
- `last_name` - фамилия

### Product (Продукт)
- `id` - уникальный идентификатор
- `title` - название продукта
- `price_cents` - цена в центах
- `stock_quantity` - количество на складе

### Order (Заказ)
- `id` - уникальный идентификатор
- `user_id` - ID пользователя
- `shipping_address_id` - ID адреса доставки
- `created_at` - дата создания
- `products` - список продуктов в заказе (many-to-many)
```
