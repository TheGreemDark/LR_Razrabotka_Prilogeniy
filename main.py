from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import engine
from models import Address, Base, Order, Product, User

Session = sessionmaker(bind=engine)

with Session() as session:
    users = session.query(User).all()
    for user in users:
        print(f"User: {user.name}, Email: {user.email}, Description: {user.decription}")
        for address in user.addresses:
            print(f"  Address: {address.city}, {address.street}")
        # Заказы этого пользователя
        orders = session.query(Order).filter(Order.user_id == user.id).all()
        for order in orders:
            print(f"  Order ID: {order.id}, Created at: {order.created_at}")
            print(
                f"    Shipping Address: {order.shipping_address.city}, {order.shipping_address.street}"
            )
            print("    Products:")
            for product in order.products:
                print(
                    f"      - {product.title}, Price: {product.price_cents / 100:.2f} USD"
                )
        print("-" * 40)
