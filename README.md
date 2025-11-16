# API Управления Пользователями

Это REST API приложение, построенное с использованием Litestar и SQLAlchemy для управления пользователями.

## Основные команды для запуска

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

2. Установка необходимых библиотек:
```bash
pip install litestar sqlalchemy aiosqlite pydantic
```

3. Инициализация базы данных:
```bash
# Создание таблиц базы данных
python init_db.py
```

4. Запуск самого приложения:
```bash
python -m app.main
```

Сервер запустится по следующему адресу `http://127.0.0.1:8000`, так как когда запускал `http://0.0.0.0:8000`, то ничего не работало.

## Проверка работоспособности API

В папке `crud_examples` находятся примеры Python-скриптов для каждой CRUD операции.
Примеры вызовов этих примеров отражены списком ниже.

1. `get_operations.py` - примеры получения данных:
   - Получение списка всех пользователей
   - Получение конкретного пользователя по ID
   ```bash
   python crud_examples/get_operations.py
   ```

2. `post_operations.py` - примеры создания новых пользователей:
   - Создание нового пользователя
   - Обработка ошибок при дублировании данных
   ```bash
   python crud_examples/post_operations.py
   ```

3. `put_operations.py` - примеры обновления данных:
   - Полное обновление пользователя
   - Частичное обновление отдельных полей
   ```bash
   python crud_examples/put_operations.py
   ```

4. `delete_operations.py` - примеры удаления данных:
   - Удаление пользователя
   - Проверка успешного удаления
   ```bash
   python crud_examples/delete_operations.py
   ```

Каждый файл содержит подробные комментарии и примеры использования. 
Перед запуском примеров необходимо проверить, что:
1. Сервер запущен (`python -m app.main`)
2. База данных инициализирована (`python init_db.py`)
3. Установлен пакет requests (`pip install requests`)

## API Endpoints (Конечные точки API)

API Endpoints - это URL-адреса, по которым можно выполнять различные операции с данными. В приложении доступны следующие endpoints:

### 1. Получение списка пользователей
- Метод: `GET`
- URL: `http://127.0.0.1:8000/users`
- Описание:
  Возвращает список всех пользователей
- Использование:
  Откройте URL в браузере или выполните GET-запрос

### 2. Получение конкретного пользователя
- Метод: `GET`
- URL: `http://127.0.0.1:8000/users/{user_id}`
  Возвращает информацию о пользователе по его ID
- Пример использование:
  `http://127.0.0.1:8000/users/1` - получить пользователя с ID=1

### 3. Создание нового пользователя
- Метод: `POST`
- URL: `http://127.0.0.1:8000/users`
- Тело запроса (пример):
```json
{
    "username": "Loken_X", 
    "email": "Loken_X_Istvaan_III@example.com",
    "full_name": "Локен Хорусович"
}
```
- Отправьте POST-запрос с JSON-данными (можно использовать Postman или curl)

### 4. Обновление пользователя
- Метод: `PUT`
- URL: `http://127.0.0.1:8000/users/{user_id}`
- Тело запроса (пример):
```json
{
    "username": "Cerberus_updated",
    "email": "Cerberus.new_Out@example.com",
    "full_name": "Церберус Новый как с завода"
}
```
- Как использовать: Отправьте PUT-запрос с JSON-данными для обновления пользователя с указанным ID

### 5. Удаление пользователя
- Метод: `DELETE`
- URL: `http://127.0.0.1:8000/users/{user_id}`
- Описание:
  Удаляет пользователя с указанным ID
- Как использовать:
  Отправьте DELETE-запрос на URL с ID пользователя

## Тестирование API

1. Использование CURL (в командной строке Windows PowerShell):

### Получение всех пользователей:
```powershell
curl http://127.0.0.1:8000/users
```

### Получение конкретного пользователя (например, с ID=1):
```powershell
curl http://127.0.0.1:8000/users/1
```

### Создание нового пользователя:
```powershell
$body = @{
    username = "Loken_X"
    email = "Loken_X_Istvaan_III@example.com"
    full_name = "Локен Хорусович"
} | ConvertTo-Json

curl -X POST http://127.0.0.1:8000/users `
     -H "Content-Type: application/json" `
     -d $body
```

### Обновление пользователя (например, с ID=1):
```powershell
$body = @{
    username = "Cerberus_updated"
    email = "Cerberus.new_Out@example.com"
    full_name = "Церберус Новый как с завода"
} | ConvertTo-Json

curl -X PUT http://127.0.0.1:8000/users/1 `
     -H "Content-Type: application/json" `
     -d $body
```

### Удаление пользователя (например, с ID=1):
```powershell
curl -X DELETE http://127.0.0.1:8000/users/1
```

Для командной строки Linux/Mac используйте обратный слэш (\) вместо backtick (`) для переноса строк:
```bash
curl -X POST http://127.0.0.1:8000/users \
     -H "Content-Type: application/json" \
     -d '{"username": "Loken_X", "email": "Loken_X_Istvaan_III@example.com", "full_name": "Локен Хорусович"}'
```

2. Используя Postman:
- Установите Postman (https://www.postman.com/downloads/)
- Создайте новый запрос, выберите метод (GET, POST, PUT, DELETE)
- Введите URL
- Для POST и PUT запросов добавьте тело запроса во вкладке "Body" в формате JSON
- Нажмите "Send"

3. Используя браузер:
- GET запросы можно выполнять прямо в браузере, просто введя URL
- Для остальных методов нужно использовать специальные инструменты (Postman, curl или расширения браузера)
```

Файл parsed_tasks.json случайно сюда попал, к данной работе он не относится.
