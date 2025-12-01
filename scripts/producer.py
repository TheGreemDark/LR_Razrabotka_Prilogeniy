import asyncio
from faststream.rabbit import RabbitBroker

broker = RabbitBroker("amqp://guest:guest@localhost:5672/local")


async def main():
    products = [
        {"id": 1, "title": "Товар 1", "price_cents": 1000, "quantity_tovar": 5},
        {"id": 2, "title": "Товар 2", "price_cents": 1500, "quantity_tovar": 3},
        {"id": 3, "title": "Товар 3", "price_cents": 2000, "quantity_tovar": 0},
        {"id": 4, "title": "Товар 4", "price_cents": 2500, "quantity_tovar": 10},
        {"id": 5, "title": "Товар 5", "price_cents": 3000, "quantity_tovar": 1},
    ]

    orders = [
        {"user_id": 1, "shipping_address_id": 1, "product_ids": [1, 2]},
        {"user_id": 2, "shipping_address_id": 1, "product_ids": [3, 4]},
        {"user_id": 3, "shipping_address_id": 2, "product_ids": [5]},
    ]

    async with broker:
        for p in products:
            await broker.publish(p, "product")
            print(f"Отправлен продукт {p['id']}")

        for o in orders:
            await broker.publish(o, "order")
            print(f"Отправлен заказ с товарами {o['product_ids']}")


if __name__ == "__main__":
    asyncio.run(main())