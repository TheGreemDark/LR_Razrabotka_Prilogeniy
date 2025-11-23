from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import *
from models import *

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

with Session() as session:
    # Пользователи
    user1 = User(name="Tarik Torgaddon", email="tarik@example.com")
    user2 = User(name="Lena Morozova", email="lena@example.com")
    user3 = User(name="Igor Smirnov", email="igor@example.com")
    user4 = User(name="Svetlana Petrova", email="svetlana@example.com")
    user5 = User(name="Maksim Volkov", email="maksim@example.com")

    session.add_all([user1, user2, user3, user4, user5])
    session.flush()  # Чтобы получить user.id для address и orders

    # Адреса
    addr1 = Address(user_id=user1.id, city="Sochi", street="Kurortny Ave, 25")
    addr2 = Address(user_id=user2.id, city="Vladivostok", street="Okeanskiy St, 10")
    addr3 = Address(user_id=user3.id, city="Omsk", street="Karla Marksa St, 7")
    addr4 = Address(user_id=user4.id, city="Ufa", street="Lenina St, 15A")
    addr5 = Address(user_id=user5.id, city="Rostov-on-Don", street="Pushkina Ave, 22")

    session.add_all([addr1, addr2, addr3, addr4, addr5])
    session.flush()

    # Продукты
    product1 = Product(title="Wireless Mouse", price_cents=1999)
    product2 = Product(title="Mechanical Keyboard", price_cents=4999)
    product3 = Product(title="USB-C Hub", price_cents=2499)
    product4 = Product(title="27-inch Monitor", price_cents=15999)
    product5 = Product(title="Gaming Chair", price_cents=8999)

    session.add_all([product1, product2, product3, product4, product5])
    session.flush()

    # Заказы
    order1 = Order(
        user_id=user1.id,
        shipping_address_id=addr1.id,
        created_at=datetime.now(),
        products=[product1, product4],
    )
    order2 = Order(
        user_id=user2.id,
        shipping_address_id=addr2.id,
        created_at=datetime.now(),
        products=[product2],
    )
    order3 = Order(
        user_id=user3.id,
        shipping_address_id=addr3.id,
        created_at=datetime.now(),
        products=[product1, product3, product5],
    )
    order4 = Order(
        user_id=user4.id,
        shipping_address_id=addr4.id,
        created_at=datetime.now(),
        products=[product3, product4],
    )
    order5 = Order(
        user_id=user5.id,
        shipping_address_id=addr5.id,
        created_at=datetime.now(),
        products=[product2, product5],
    )

    session.add_all([order1, order2, order3, order4, order5])

    session.commit()
