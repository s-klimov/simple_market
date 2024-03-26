from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy

from database import Base
from sqlalchemy.orm import relationship, Mapped


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "main"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, unique=True)

    # Relationships
    orders = relationship("Order", back_populates="user")


# https://www.gormanalysis.com/blog/many-to-many-relationships-in-fastapi/
class OrderProduct(Base):
    __tablename__ = "order_product"
    __table_args__ = {"schema": "main"}

    order_id = Column(ForeignKey("main.order.id"), primary_key=True)
    product_id = Column(ForeignKey("main.product.id"), primary_key=True)
    count = Column(Integer, nullable=False, default=1)

    # Relationships
    order = relationship("Order", back_populates="products")
    product = relationship("Product", back_populates="orders")

    # proxies
    order_user = association_proxy(target_collection="order", attr="user.id")
    product_name = association_proxy(target_collection="product", attr="name")


class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": "main"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, unique=True)

    # Relationships
    orders: Mapped[OrderProduct] = relationship(
        "OrderProduct", back_populates="product", lazy="selectin"
    )


class Order(Base):
    __tablename__ = "order"
    __table_args__ = {"schema": "main"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("main.user.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="orders", lazy="selectin")
    products = relationship("OrderProduct", back_populates="order", lazy="selectin")
