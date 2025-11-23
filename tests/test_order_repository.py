import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.schemas.user_schema import UserCreate
from models import Address, Order, Product


@pytest.mark.asyncio
async def test_create_order_with_multiple_products(
    session, user_repository, product_repository, order_repository
):
    # Создаём пользователя через репозиторий
    user = await user_repository.create(
        UserCreate(
            email="u1@example.com", username="u1", first_name="U1", last_name="Test"
        )
    )

    # Создаём и сохраняем адрес пользователя через сессию
    addr = Address(user_id=user.id, city="City", street="Street 1")
    session.add(addr)
    await session.commit()
    await session.refresh(addr)

    # Создаём два продукта через репозиторий
    p1 = await product_repository.create("Prod A", 1000, 10)
    p2 = await product_repository.create("Prod B", 2000, 5)

    # Создаём заказ пользователя с двумя продуктами
    order = await order_repository.create(user.id, addr.id, [p1.id, p2.id])

    # Проверяем, что заказ создан и содержит оба продукта
    assert order is not None
    assert len(order.products) == 2
    ids = {p.id for p in order.products}
    assert ids == {p1.id, p2.id}


@pytest.mark.asyncio
async def test_create_order_with_missing_product_ids(
    session, user_repository, product_repository, order_repository
):
    # Создаём пользователя для теста
    user = await user_repository.create(
        UserCreate(
            email="u2@example.com", username="u2", first_name="U2", last_name="Test"
        )
    )
    # Создаём и сохраняем адрес
    addr = Address(user_id=user.id, city="City", street="Street 2")
    session.add(addr)
    await session.commit()
    await session.refresh(addr)

    # Создаём один существующий продукт
    p1 = await product_repository.create("Prod C", 500, 3)

    # Пытаемся создать заказ с одним валидным и одним несуществующим ID продукта
    order = await order_repository.create(user.id, addr.id, [p1.id, 99999])

    # Проверяем, что заказ создан, но содержит только существующий продукт
    assert order is not None
    assert len(order.products) == 1
    assert order.products[0].id == p1.id


@pytest.mark.asyncio
async def test_create_order_with_duplicate_product_ids(
    session, user_repository, product_repository, order_repository
):
    # Создаём пользователя и адрес
    user = await user_repository.create(
        UserCreate(
            email="u3@example.com", username="u3", first_name="U3", last_name="Test"
        )
    )
    addr = Address(user_id=user.id, city="City", street="Street 3")
    session.add(addr)
    await session.commit()
    await session.refresh(addr)

    # Создаём продукт
    p1 = await product_repository.create("Prod D", 1500, 2)

    # Создаём заказ с дублирующимися ID продукта
    order = await order_repository.create(user.id, addr.id, [p1.id, p1.id])

    # Проверяем, что продукт добавлен только один раз
    assert order is not None
    assert len(order.products) == 1
    assert order.products[0].id == p1.id


@pytest.mark.asyncio
async def test_add_product_already_in_order(
    session, user_repository, product_repository, order_repository
):
    # Создаём пользователя, адрес и продукт
    user = await user_repository.create(
        UserCreate(
            email="u4@example.com", username="u4", first_name="U4", last_name="Test"
        )
    )
    addr = Address(user_id=user.id, city="City", street="Street 4")
    session.add(addr)
    await session.commit()
    await session.refresh(addr)

    p1 = await product_repository.create("Prod E", 1200, 4)

    # Создаём заказ с одним продуктом
    order = await order_repository.create(user.id, addr.id, [p1.id])
    # Пытаемся добавить тот же продукт повторно
    order = await order_repository.add_product(order.id, p1.id)

    # Проверяем, что продукт не дублируется
    assert len(order.products) == 1


@pytest.mark.asyncio
async def test_remove_product_not_in_order(
    session, user_repository, product_repository, order_repository
):
    # Создаём пользователя и адрес
    user = await user_repository.create(
        UserCreate(
            email="u5@example.com", username="u5", first_name="U5", last_name="Test"
        )
    )
    addr = Address(user_id=user.id, city="City", street="Street 5")
    session.add(addr)
    await session.commit()
    await session.refresh(addr)

    # Создаём два продукта
    p1 = await product_repository.create("Prod F", 700, 6)
    p2 = await product_repository.create("Prod G", 800, 1)

    # Создаём заказ с одним продуктом (p1)
    order = await order_repository.create(user.id, addr.id, [p1.id])

    # Пытаемся удалить продукт (p2), которого нет в заказе
    order_after = await order_repository.remove_product(order.id, p2.id)

    # Проверяем, что заказ остался без изменений
    assert len(order_after.products) == 1
    assert order_after.products[0].id == p1.id


@pytest.mark.asyncio
async def test_create_order_with_empty_products(
    session, user_repository, order_repository
):
    user = await user_repository.create(
        UserCreate(
            email="u6@example.com", username="u6", first_name="U6", last_name="Test"
        )
    )
    addr = Address(user_id=user.id, city="City", street="Street 6")
    session.add(addr)
    await session.commit()
    await session.refresh(addr)

    order = await order_repository.create(user.id, addr.id, [])
    assert order is not None
    assert len(order.products) == 0


# Тест получения всех заказов конкретного пользователя с продуктами по user_id
@pytest.mark.asyncio
async def test_get_by_user(
    session, user_repository, product_repository, order_repository
):
    # Создаём пользователя
    user = await user_repository.create(
        UserCreate(
            email="byuser@example.com",
            username="userA",
            first_name="UserA",
            last_name="Test",
        )
    )
    addr = Address(user_id=user.id, city="CityU", street="StreetU")
    session.add(addr)
    await session.commit()
    await session.refresh(addr)
    prod1 = await product_repository.create("ProdU1", 300, 6)
    prod2 = await product_repository.create("ProdU2", 500, 7)
    order1 = await order_repository.create(user.id, addr.id, [prod1.id])
    order2 = await order_repository.create(user.id, addr.id, [prod2.id])

    # Получаем все заказы этого пользователя, подгружая связанные продукты
    stmt = select(Order).where(Order.user_id == user.id).options()
    result = await session.execute(stmt)
    orders = result.scalars().all()
    assert len(orders) >= 2
    # Проверяем, что в каждом заказе есть связанные продукты
    for order in orders:
        assert hasattr(order, "products")
        assert len(order.products) >= 1


# Тест получения заказа по id с подгрузкой связанных продуктов
@pytest.mark.asyncio
async def test_get_by_id(
    session, user_repository, product_repository, order_repository
):
    # Создаём пользователя, адрес, продукты и заказ
    user = await user_repository.create(
        UserCreate(
            email="byid@example.com",
            username="userB",
            first_name="UserB",
            last_name="Test",
        )
    )
    addr = Address(user_id=user.id, city="CityB", street="StreetB")
    session.add(addr)
    await session.commit()
    await session.refresh(addr)
    prod1 = await product_repository.create("ProdI1", 500, 8)
    prod2 = await product_repository.create("ProdI2", 600, 9)
    order = await order_repository.create(user.id, addr.id, [prod1.id, prod2.id])

    # Получаем заказ по id c подгруженными продуктами
    stmt = select(Order).where(Order.id == order.id)
    result = await session.execute(stmt)
    fetched_order = result.scalars().first()
    assert fetched_order is not None
    assert hasattr(fetched_order, "products")
    assert {p.id for p in fetched_order.products} == {prod1.id, prod2.id}


@pytest.mark.asyncio
async def test_delete_order_by_id(
    session, user_repository, product_repository, order_repository
):
    """
    Тест удаления заказа по его ID.
    Проверяет, что заказ удаляется корректно, если существует.
    """
    # Создаём пользователя, адрес и заказ
    user = await user_repository.create(
        UserCreate(
            email="delorder@example.com",
            username="delU",
            first_name="Del",
            last_name="User",
        )
    )
    addr = Address(user_id=user.id, city="CityDel", street="StreetDel")
    session.add(addr)
    await session.commit()
    await session.refresh(addr)
    prod = await product_repository.create("ProdDel", 900, 1)
    order = await order_repository.create(user.id, addr.id, [prod.id])

    # Удаляем заказ по ID
    await order_repository.delete(order.id)

    # Пытаемся получить заказ после удаления
    stmt = select(Order).where(Order.id == order.id)
    result = await session.execute(stmt)
    deleted_order = result.scalars().first()
    assert deleted_order is None


@pytest.mark.asyncio
async def test_get_all_order(session, order_repository):
    """
    Тест получения всех заказов с подгрузкой связанных продуктов.
    Проверяется, что возвращенный список содержит заказы с продуктами.
    """
    # Получение всех заказов с жадной загрузкой связанных продуктов
    stmt = select(Order).options(selectinload(Order.products))
    result = await session.execute(stmt)
    orders = result.scalars().all()

    assert isinstance(orders, list)
    # Проверяем, что у каждого заказа есть связанные продукты (может быть пустой список)
    for order in orders:
        assert hasattr(order, "products")
        assert isinstance(order.products, list)


@pytest.mark.asyncio
async def test_get_all_product(session, product_repository):
    """
    Тест получения полного списка продуктов.
    Проверяется, что список не пустой и содержит объекты Product.
    """
    # Получение всех продуктов
    stmt = select(Product)
    result = await session.execute(stmt)
    products = result.scalars().all()

    assert isinstance(products, list)
    assert len(products) > 0
    assert all(isinstance(p, Product) for p in products)
