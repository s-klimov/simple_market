from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy

from database import Base
from sqlalchemy.orm import relationship, backref


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "main"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, unique=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    disable = Column(Boolean)

    # Relationships
    orders = relationship("Order", backref=backref("user", lazy="joined"))


# https://www.gormanalysis.com/blog/many-to-many-relationships-in-fastapi/
class OrderProduct(Base):
    __tablename__ = "order_product"
    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="order_product_unique"),
        {"schema": "main"},
    )

    order_id = Column(ForeignKey("main.order.id"), primary_key=True)
    product_id = Column(ForeignKey("main.product.id"), primary_key=True)
    count = Column(Integer, nullable=False, default=1)

    # Relationships
    order = relationship("Order", back_populates="cart")
    product = relationship("Product", back_populates="cart")


class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": "main"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, unique=True)

    # Relationships
    cart = relationship("OrderProduct", back_populates="product", lazy="selectin")

    # proxies
    products = association_proxy("cart", "order")


class Order(Base):
    __tablename__ = "order"
    __table_args__ = {"schema": "main"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("main.user.id"), nullable=False)

    # Relationships
    cart = relationship("OrderProduct", back_populates="order", lazy="selectin")

    # proxies
    products = association_proxy("cart", "product")
