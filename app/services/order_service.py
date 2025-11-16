from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.schemas.order_product_schema import OrderCreate, OrderUpdate
from models import Order

class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
        user_repository: UserRepository,
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.user_repository = user_repository

    async def get_by_id(self, order_id: int) -> Order | None:
        return await self.order_repository.get_by_id(order_id)

    async def get_by_filter(self, count: int = 10, page: int = 1, **filters) -> list[Order]:
        return await self.order_repository.get_by_filter(count=count, page=page, **filters)

    # Новый метод для создания заказа с несколькими товарами в формате из теста
    async def create_order(self, order_data: dict) -> Order:
        user = await self.user_repository.get_by_id(order_data['user_id'])
        if not user:
            raise ValueError("Пользователь не найден")

        total_amount = 0
        # Проверяем все товары в заказе
        for item in order_data['items']:
            product = await self.product_repository.get_by_id(item['product_id'])
            if not product:
                raise ValueError(f"Товар с id {item['product_id']} не найден")
            if product.stock_quantity < item['quantity']:
                raise ValueError("Insufficient stock")
            total_amount += product.price * item['quantity']

        # Создаём объект OrderCreate (пример, в зависимости от вашей модели)
        order_create = OrderCreate(
            user_id=order_data['user_id'],
            total_amount=total_amount,
            status="pending",
            # возможно нужно передать товары в заказ, зависит от схемы
        )
        order = await self.order_repository.create(order_create)

        # Логика для сохранения позиций заказа (если нужно)

        return order

    async def create(self, order_data: OrderCreate) -> Order:
        # Старый метод создания одного товара
        ...

    async def update(self, order_id: int, order_data: OrderUpdate) -> Order | None:
        return await self.order_repository.update(order_id, order_data)

    async def delete(self, order_id: int) -> None:
        await self.order_repository.delete(order_id)
