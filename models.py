# models.py
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class UserCreate(BaseModel):
    email: str
    password: str
    # другие поля


class UserUpdate(BaseModel):
    email: str | None = None
    password: str | None = None
    # другие поля для обновления


class UserResponse(BaseModel):
    id: int
    email: str
    # другие поля


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))

    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    city = Column(String(100), nullable=False)
    street = Column(String(200), nullable=False)

    user = relationship("User", back_populates="addresses")


# Расширение: товары и заказы
from sqlalchemy import DateTime, Table, func

# Многие-ко-многим между заказом и продуктами
order_products = Table(
    "order_products",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True),
)


# Продукт и ордер, в продукт добавлено поле quantity_tovar
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    price_cents = Column(Integer, nullable=False)
    quantity_tovar = Column(Integer, nullable=False, default=0)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    shipping_address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User")
    shipping_address = relationship("Address")
    products = relationship("Product", secondary=order_products, lazy="selectin")
