from unittest.mock import AsyncMock, MagicMock, PropertyMock

import pytest

from app.services.order_service import OrderService


@pytest.mark.asyncio
class TestOrderService:

    async def test_create_order_insufficient_stock(self):
        # Создаём моки репозиториев
        mock_order_repo = AsyncMock()
        mock_product_repo = AsyncMock()
        mock_user_repo = AsyncMock()

        # Мок пользователя
        mock_user_repo.get_by_id.return_value = MagicMock(id=1)

        # Мок продукта с property stock_quantity = 1
        mock_product = MagicMock()
        type(mock_product).stock_quantity = PropertyMock(return_value=1)
        mock_product_repo.get_by_id.return_value = mock_product

        # Инициализируем OrderService с моками
        order_service = OrderService(
            order_repository=mock_order_repo,
            product_repository=mock_product_repo,
            user_repository=mock_user_repo,
        )

        order_data = {
            "user_id": 1,
            "items": [
                {"product_id": 1, "quantity": 2}
            ],  # quantity больше stock_quantity
        }

        with pytest.raises(ValueError, match="Insufficient stock"):
            await order_service.create_order(order_data)
