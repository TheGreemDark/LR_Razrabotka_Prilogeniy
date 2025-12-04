"""
Тестирование кэширования пользователей и продуктов
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.user_schema import UserCreate, UserUpdate
from app.redis_cache import get_redis_cache


async def test_user_caching():
    """Тест кэширования пользователей"""
    print("\n")
    print("Тест кэширования пользователей")
    
    # Подключение к БД
    engine = create_async_engine("sqlite+aiosqlite:///mydb.sqlite3", echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        repo = UserRepository()
        repo.session = session
        
        # Очищаем кэш перед тестами
        cache = get_redis_cache()
        cache.clear_pattern("user:*")
        print("\n[CACHE CLEAR] Очистка кэша пользователей перед тестами")
        
        # 1. Создаём тестового пользователя
        print("\n1. Создание пользователя...")
        user_data = UserCreate(
            username="Lokencache_test_user",
            email="Lokencache@test.com",
            first_name="Cache",
            last_name="LokenTest"
        )
        user = await repo.create(user_data)
        print(f"   Создан пользователь ID: {user.id}")
        
        # 2. Первое получение (из БД - CACHE MISS)
        print("\n2. Первое получение пользователя (должен быть CACHE MISS):")
        user1 = await repo.get_by_id(user.id)
        print(f"   Получен: {user1.username}, {user1.email}")
        
        # 3. Второе получение (из кэша - CACHE HIT)
        print("\n3. Второе получение пользователя (должен быть CACHE HIT):")
        user2 = await repo.get_by_id(user.id)
        print(f"   Получен: {user2.username}, {user2.email}")
        
        # 4. Обновление пользователя (должен удалить из кэша)
        print("\n4. Обновление пользователя...")
        update_data = UserUpdate(
            first_name="Updated", 
            last_name="Name"
        )
        await repo.update(user.id, update_data)
        
        # 5. Получение после обновления (из БД - CACHE MISS)
        print("\n5. Получение после обновления (должен быть CACHE MISS):")
        user3 = await repo.get_by_id(user.id)
        print(f"   Получен: {user3.username}, {user3.first_name} {user3.last_name}")
        
        # 6. Удаление пользователя
        print("\n6. Удаление пользователя...")
        await repo.delete(user.id)
        
        print("\nТест кэширования пользователей завершён успешно!")


async def test_product_caching():
    """Тест кэширования продуктов"""
    print("\n")
    print("Тест кэширования продуктов")
    print("=")
    
    # Подключение к БД
    engine = create_async_engine("sqlite+aiosqlite:///mydb.sqlite3", echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        repo = ProductRepository(session)
        
        # Очищаем кэш перед тестами
        cache = get_redis_cache()
        cache.clear_pattern("product:*")
        print("\n[CACHE CLEAR] Очистили кэш продуктов перед тестами")
        
        # 1. Создаём тестовый продукт
        print("\n1. Создание продукта...")
        product = await repo.create("Cache Test Product", 5000, 100)
        print(f"   Создан продукт ID: {product.id}")
        
        # 2. Первое получение (из БД - CACHE MISS)
        print("\n2. Первое получение продукта (должен быть CACHE MISS):")
        prod1 = await repo.get_by_id(product.id)
        print(f"   Получен: {prod1.title}, Stock: {prod1.quantity_tovar}") 
        
        # 3. Второе получение (из кэша - CACHE HIT)
        print("\n3. Второе получение продукта (должен быть CACHE HIT):")
        prod2 = await repo.get_by_id(product.id)
        print(f"   Получен: {prod2.title}, Stock: {prod2.quantity_tovar}") 
        
        # 4. Обновление остатков (должен обновить кэш)
        print("\n4. Обновление остатков продукта...")
        await repo.update_stock(product.id, 50)
        
        # 5. Получение после обновления (из кэша с новыми данными - CACHE HIT)
        print("\n5. Получение после обновления (должен быть CACHE HIT с новыми данными):")
        prod3 = await repo.get_by_id(product.id)
        print(f"   Получен: {prod3.title}, Stock: {prod3.quantity_tovar}") 
        
        # 6. Удаление продукта
        print("\n6. Удаление продукта...")
        await repo.delete(product.id)
        
        print("\nТестирование продуктов завершёно успешно!")


async def main():
    print("\n")
    print("Запуск тестов")
    print("="*60)
    
    await test_user_caching()
    await test_product_caching()
    
    print("\n")
    print("Все тесты выполнены корректно!")
    print("\n")


if __name__ == "__main__":
    asyncio.run(main())