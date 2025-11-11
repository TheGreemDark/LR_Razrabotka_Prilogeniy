# seed.py
from db import SessionLocal
from models import User, Address
from models import Product, Order, User

def seed():
    with SessionLocal() as session:
        users = []
        for i in range(1, 6):
            u = User(name=f"User {i}", email=f"user{i}@example.com")
            u.addresses = [
                Address(city="CityA", street=f"A Street {i}"),
                Address(city="CityB", street=f"B Street {i}")
            ]
            users.append(u)
        session.add_all(users)
        session.commit()
def seed_products_and_orders():
    with SessionLocal() as session:
        products = [
            Product(title="Prod A", price_cents=1000),
            Product(title="Prod B", price_cents=1500),
            Product(title="Prod C", price_cents=2000),
            Product(title="Prod D", price_cents=2500),
            Product(title="Prod E", price_cents=3000),
        ]
        session.add_all(products)
        session.commit()

        user = session.query(User).first()
        addr = user.addresses[0]
        prods = session.query(Product).all()

        order = Order(user=user, shipping_address=addr, products=prods[:2])
        session.add(order)
        session.commit()
if __name__ == "__main__":
    seed()