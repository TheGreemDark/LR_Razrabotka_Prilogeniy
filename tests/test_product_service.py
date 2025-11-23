from unittest.mock import AsyncMock, Mock

import pytest
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate
from app.services.order_service import OrderService
from models import Address, Order, Product


class TestOrderServiceWithMock:
    @pytest.mark.asyncio
    async def test_create_order_with_multiple_products(self):
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_order_repo = AsyncMock(spec=OrderRepository)

        mock_user = Mock(
            id=1,
            email="u1@example.com",
            username="u1",
            first_name="U1",
            last_name="Test",
        )
        mock_addr = Mock(id=1, user_id=1, city="City", street="Street 1")
        mock_p1 = Mock(id=1, name="Prod A", price=1000, quantity_tovar=10)
        mock_p2 = Mock(id=2, name="Prod B", price=2000, quantity_tovar=5)
        mock_order = Mock(
            id=1,
            user_id=mock_user.id,
            address_id=mock_addr.id,
            products=[mock_p1, mock_p2],
        )

        mock_user_repo.create.return_value = mock_user
        mock_product_repo.create.side_effect = [mock_p1, mock_p2]
        mock_order_repo.create.return_value = mock_order

        service = OrderService(
            user_repository=mock_user_repo,
            product_repository=mock_product_repo,
            order_repository=mock_order_repo,
        )

        user = await service.user_repository.create(
            UserCreate(
                email="u1@example.com", username="u1", first_name="U1", last_name="Test"
            )
        )
        p1 = await service.product_repository.create("Prod A", 1000, 10)
        p2 = await service.product_repository.create("Prod B", 2000, 5)
        order = await service.order_repository.create(
            user.id, mock_addr.id, [p1.id, p2.id]
        )

        mock_user_repo.create.assert_awaited_once()
        mock_product_repo.create.assert_awaited()
        mock_order_repo.create.assert_awaited_once_with(
            user.id, mock_addr.id, [p1.id, p2.id]
        )
        assert order is not None
        assert len(order.products) == 2
        assert {p.id for p in order.products} == {p1.id, p2.id}

    @pytest.mark.asyncio
    async def test_create_order_with_missing_product_ids(self):
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_order_repo = AsyncMock(spec=OrderRepository)

        mock_user = Mock(id=2)
        mock_addr = Mock(id=2, user_id=2, city="City", street="Street 2")
        mock_p1 = Mock(id=3, name="Prod C", price=500, quantity_tovar=3)
        mock_order = Mock(
            id=2, user_id=mock_user.id, address_id=mock_addr.id, products=[mock_p1]
        )

        mock_user_repo.create.return_value = mock_user
        mock_product_repo.create.return_value = mock_p1
        mock_order_repo.create.return_value = mock_order

        service = OrderService(
            user_repository=mock_user_repo,
            product_repository=mock_product_repo,
            order_repository=mock_order_repo,
        )

        user = await service.user_repository.create(
            UserCreate(
                email="u2@example.com", username="u2", first_name="U2", last_name="Test"
            )
        )
        p1 = await service.product_repository.create("Prod C", 500, 3)
        order = await service.order_repository.create(
            user.id, mock_addr.id, [p1.id, 99999]
        )

        mock_order_repo.create.assert_awaited_once_with(
            user.id, mock_addr.id, [p1.id, 99999]
        )
        assert order is not None
        assert len(order.products) == 1
        assert order.products[0].id == p1.id

    @pytest.mark.asyncio
    async def test_create_order_with_duplicate_product_ids(self):
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_order_repo = AsyncMock(spec=OrderRepository)

        mock_user = Mock(id=3)
        mock_addr = Mock(id=3, user_id=3, city="City", street="Street 3")
        mock_p1 = Mock(id=4, name="Prod D", price=1500, quantity_tovar=2)
        mock_order = Mock(
            id=3, user_id=mock_user.id, address_id=mock_addr.id, products=[mock_p1]
        )

        mock_user_repo.create.return_value = mock_user
        mock_product_repo.create.return_value = mock_p1
        mock_order_repo.create.return_value = mock_order

        service = OrderService(
            user_repository=mock_user_repo,
            product_repository=mock_product_repo,
            order_repository=mock_order_repo,
        )

        user = await service.user_repository.create(
            UserCreate(
                email="u3@example.com", username="u3", first_name="U3", last_name="Test"
            )
        )
        p1 = await service.product_repository.create("Prod D", 1500, 2)
        order = await service.order_repository.create(
            user.id, mock_addr.id, [p1.id, p1.id]
        )

        mock_order_repo.create.assert_awaited_once_with(
            user.id, mock_addr.id, [p1.id, p1.id]
        )
        assert order is not None
        assert len(order.products) == 1
        assert order.products[0].id == p1.id

    @pytest.mark.asyncio
    async def test_add_product_already_in_order(self):
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_order_repo = AsyncMock(spec=OrderRepository)

        mock_user = Mock(id=4)
        mock_addr = Mock(id=4, user_id=4, city="City", street="Street 4")
        mock_p1 = Mock(id=5, name="Prod E", price=1200, quantity_tovar=4)
        mock_order = Mock(
            id=4, user_id=mock_user.id, address_id=mock_addr.id, products=[mock_p1]
        )

        mock_user_repo.create.return_value = mock_user
        mock_product_repo.create.return_value = mock_p1
        mock_order_repo.create.return_value = mock_order
        mock_order_repo.add_product.return_value = mock_order

        service = OrderService(
            user_repository=mock_user_repo,
            product_repository=mock_product_repo,
            order_repository=mock_order_repo,
        )

        user = await service.user_repository.create(
            UserCreate(
                email="u4@example.com", username="u4", first_name="U4", last_name="Test"
            )
        )
        p1 = await service.product_repository.create("Prod E", 1200, 4)
        order = await service.order_repository.create(user.id, mock_addr.id, [p1.id])
        order = await service.order_repository.add_product(order.id, p1.id)

        mock_order_repo.add_product.assert_awaited_once_with(order.id, p1.id)
        assert len(order.products) == 1

    @pytest.mark.asyncio
    async def test_create_order_with_empty_products(self):
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)

        mock_user = Mock(id=6)
        mock_addr = Mock(id=6, user_id=6, city="City", street="Street 6")
        mock_order = Mock(
            id=6, user_id=mock_user.id, address_id=mock_addr.id, products=[]
        )

        mock_user_repo.create.return_value = mock_user
        mock_order_repo.create.return_value = mock_order

        service = OrderService(
            user_repository=mock_user_repo,
            product_repository=mock_product_repo,
            order_repository=mock_order_repo,
        )

        user = await service.user_repository.create(
            UserCreate(
                email="u6@example.com", username="u6", first_name="U6", last_name="Test"
            )
        )
        order = await service.order_repository.create(user.id, mock_addr.id, [])

        mock_order_repo.create.assert_awaited_once()
        assert order is not None
        assert len(order.products) == 0

    @pytest.mark.asyncio
    async def test_get_by_user(self):
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_order_repo = AsyncMock(spec=OrderRepository)

        mock_user = Mock(id=7)
        mock_addr = Mock(id=7, user_id=7, city="CityU", street="StreetU")
        mock_prod1 = Mock(id=8, name="ProdU1", price=300, quantity_tovar=6)
        mock_prod2 = Mock(id=9, name="ProdU2", price=500, quantity_tovar=7)
        mock_order1 = Mock(
            id=7, user_id=mock_user.id, address_id=mock_addr.id, products=[mock_prod1]
        )
        mock_order2 = Mock(
            id=8, user_id=mock_user.id, address_id=mock_addr.id, products=[mock_prod2]
        )

        mock_user_repo.create.return_value = mock_user
        mock_product_repo.create.side_effect = [mock_prod1, mock_prod2]
        mock_order_repo.create.side_effect = [mock_order1, mock_order2]

        service = OrderService(
            user_repository=mock_user_repo,
            product_repository=mock_product_repo,
            order_repository=mock_order_repo,
        )

        user = await service.user_repository.create(
            UserCreate(
                email="byuser@example.com",
                username="userA",
                first_name="UserA",
                last_name="Test",
            )
        )
        p1 = await service.product_repository.create("ProdU1", 300, 6)
        p2 = await service.product_repository.create("ProdU2", 500, 7)
        order1 = await service.order_repository.create(user.id, mock_addr.id, [p1.id])
        order2 = await service.order_repository.create(user.id, mock_addr.id, [p2.id])

        orders = [order1, order2]

        assert len(orders) >= 2
        for order in orders:
            assert hasattr(order, "products")
            assert len(order.products) >= 1

    @pytest.mark.asyncio
    async def test_get_by_id(self):
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_order_repo = AsyncMock(spec=OrderRepository)

        mock_user = Mock(id=10)
        mock_addr = Mock(id=10, user_id=10, city="CityB", street="StreetB")
        mock_prod1 = Mock(id=11, name="ProdI1", price=500, quantity_tovar=8)
        mock_prod2 = Mock(id=12, name="ProdI2", price=600, quantity_tovar=9)
        mock_order = Mock(
            id=9,
            user_id=mock_user.id,
            address_id=mock_addr.id,
            products=[mock_prod1, mock_prod2],
        )

        mock_user_repo.create.return_value = mock_user
        mock_product_repo.create.side_effect = [mock_prod1, mock_prod2]
        mock_order_repo.create.return_value = mock_order

        service = OrderService(
            user_repository=mock_user_repo,
            product_repository=mock_product_repo,
            order_repository=mock_order_repo,
        )

        user = await service.user_repository.create(
            UserCreate(
                email="byid@example.com",
                username="userB",
                first_name="UserB",
                last_name="Test",
            )
        )
        p1 = await service.product_repository.create("ProdI1", 500, 8)
        p2 = await service.product_repository.create("ProdI2", 600, 9)
        order = await service.order_repository.create(
            user.id, mock_addr.id, [p1.id, p2.id]
        )

        assert order is not None
        assert hasattr(order, "products")
        assert {p.id for p in order.products} == {p1.id, p2.id}

    @pytest.mark.asyncio
    async def test_delete_order_by_id(self):
        mock_user_repo = AsyncMock(spec=UserRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_order_repo = AsyncMock(spec=OrderRepository)

        mock_user = Mock(id=13)
        mock_addr = Mock(id=13, user_id=13, city="CityDel", street="StreetDel")
        mock_prod = Mock(id=14, name="ProdDel", price=900, quantity_tovar=1)
        mock_order = Mock(
            id=10, user_id=mock_user.id, address_id=mock_addr.id, products=[mock_prod]
        )

        mock_user_repo.create.return_value = mock_user
        mock_product_repo.create.return_value = mock_prod
        mock_order_repo.create.return_value = mock_order
        mock_order_repo.delete.return_value = None

        service = OrderService(
            user_repository=mock_user_repo,
            product_repository=mock_product_repo,
            order_repository=mock_order_repo,
        )

        user = await service.user_repository.create(
            UserCreate(
                email="delorder@example.com",
                username="delU",
                first_name="Del",
                last_name="User",
            )
        )
        prod = await service.product_repository.create("ProdDel", 900, 1)
        order = await service.order_repository.create(user.id, mock_addr.id, [prod.id])
        await service.order_repository.delete(order.id)

        mock_order_repo.delete.assert_awaited_once_with(order.id)
