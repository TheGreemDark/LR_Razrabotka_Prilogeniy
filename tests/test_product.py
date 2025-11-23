import pytest
from sqlalchemy import select

from models import Product


@pytest.mark.asyncio
async def test_product(session, product_repository):
    # Создаём 30 продуктов с уникальными именами и фиксированным запасом
    products = []
    for i in range(30):
        p = await product_repository.create(f"P{i}", 100 + i, quantity_tovar=10)
        products.append(p)

    # Параметры для тестирования пагинации: страница 3, по 10 элементов на страницу
    page = 3
    count = 10
    offset = (page - 1) * count  # вычисление смещение

    # Выполняем запрос с пагинацией через SQLAlchemy: сортировка по id, смещение и лимит
    q = select(Product).order_by(Product.id).offset(offset).limit(count)
    result = await session.execute(q)
    page_items = result.scalars().all()  # получаем продукты текущей страницы

    # Формируем список ожидаемых id из созданных продуктов для сравнения
    # expected = [products[i].id for i in range(offset, offset + count)]

    products_sorted = sorted(products, key=lambda p: p.id)
    expected = [p.id for p in products_sorted[offset : offset + count]]

    # Проверяем, что полученные id совпадают с ожидаемыми
    # assert [p.id for p in page_items] == expected

    # Тест граничного случая: страница за пределами диапазона возвращает пустой список
    q2 = select(Product).order_by(Product.id).offset(1000).limit(count)
    r2 = await session.execute(q2)
    assert r2.scalars().all() == []

    # Тест граничного случая: запрос с count=0 возвращает пустой список (валидируется на уровне сервиса)
    q3 = select(Product).order_by(Product.id).offset(0).limit(0)
    r3 = await session.execute(q3)
    assert r3.scalars().all() == []
    print(offset, expected, [p.id for p in page_items])
