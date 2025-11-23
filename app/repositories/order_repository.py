from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import Order, Product


class OrderRepository:
    def __init__(self, session: AsyncSession):
        # Инициализация репозитория с асинхронной сессией базы данных
        self.session = session

    async def get_by_id(self, order_id: int) -> Order | None:
        # Получение заказа по ID с подгрузкой связанных продуктов (ленивая загрузка)
        query = (
            select(Order)
            .options(selectinload(Order.products))
            .where(Order.id == order_id)
        )
        result = await self.session.execute(query)
        # Возвращается один объект Order или None, если не найден
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Order]:
        # Получение списка всех заказов с подгрузкой связанных продуктов
        query = select(Order).options(selectinload(Order.products))
        result = await self.session.execute(query)
        # Возвращаем список объектов Order
        return list(result.scalars().all())

    async def get_by_user(self, user_id: int) -> list[Order]:
        # Получение всех заказов конкретного пользователя по user_id с продуктами
        query = (
            select(Order)
            .options(selectinload(Order.products))
            .where(Order.user_id == user_id)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(
        self, user_id: int, shipping_address_id: int, product_ids: list[int]
    ) -> Order:
        # Создание нового заказа с user_id и адресом доставки
        order = Order(user_id=user_id, shipping_address_id=shipping_address_id)
        # Если есть ID продуктов - загружаем их из БД и добавляем к заказу
        if product_ids:
            query = select(Product).where(Product.id.in_(product_ids))
            result = await self.session.execute(query)
            products = list(result.scalars().all())
            order.products.extend(products)

        # Добавляем заказ в сессию и сохраняем изменения в БД
        self.session.add(order)
        await self.session.commit()
        # Обновляем объект заказа из БД, чтобы получить актуальные данные (например, ID)
        await self.session.refresh(order)
        return order

    async def add_product(self, order_id: int, product_id: int) -> Order | None:
        # Добавляем продукт к заказу по их ID
        order = await self.get_by_id(order_id)
        if not order:
            return None

        query = select(Product).where(Product.id == product_id)
        result = await self.session.execute(query)
        product = result.scalar_one_or_none()

        # Проверяем, что продукт существует и не добавлен ранее
        if product and product not in order.products:
            order.products.append(product)
            await self.session.commit()
            await self.session.refresh(order)

        return order

    async def remove_product(self, order_id: int, product_id: int) -> Order | None:
        # Удаляем продукт из заказа по ID заказа и продукта
        order = await self.get_by_id(order_id)
        if not order:
            return None

        query = select(Product).where(Product.id == product_id)
        result = await self.session.execute(query)
        product = result.scalar_one_or_none()

        # Проверяем, что продукт существует и принадлежит заказу, затем удаляем
        if product and product in order.products:
            order.products.remove(product)
            await self.session.commit()
            await self.session.refresh(order)

        return order

    async def delete(self, order_id: int) -> None:
        # Удаление заказа по ID, если он существует
        order = await self.get_by_id(order_id)
        if order:
            await self.session.delete(order)
            await self.session.commit()
