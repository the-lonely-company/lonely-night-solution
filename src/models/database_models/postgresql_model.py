from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from connections.postgresqldb.postgresql_connection import Base

class User(Base):
    """
    Represents a User in the system.
    """

    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, unique=True, index=True)
    firebase_uid = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    phone_number_prefix = Column(String)
    phone_number = Column(String, index=True)
    date_of_birth = Column(Date)
    is_merchant = Column(Boolean, default=False)

    customer_orders = relationship("CustomerOrder", back_populates="user")
    merchant = relationship("Merchant", back_populates="user", uselist=False)


class Merchant(Base):
    """
    Represents a merchant in the system.
    """
    __tablename__ = "merchant"

    merchant_id = Column(Integer, primary_key=True, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    address = Column(String, index=True)
    delivery_fee = Column(Float)

    user_id = Column(Integer, ForeignKey('user.user_id'), unique=True)

    user = relationship("User", back_populates="merchant")
    customer_orders = relationship("CustomerOrder", back_populates="merchant")


class CustomerOrder(Base):
    """
    Represents a order by a customer in the system.
    """
    __tablename__ = "customer_order"

    order_id = Column(Integer, primary_key=True, unique=True, index=True)
    reference_no = Column(Integer, unique=True, index=True)
    status = Column(String, index=True)
    date_order_placed = Column(Date)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    merchant_id = Column(Integer, ForeignKey('merchant.merchant_id'))
    total_order_amount = Column(Float)

    user = relationship("User", back_populates="customer_orders")
    merchant = relationship("Merchant", back_populates="customer_orders")

class CustomerOrderItem(Base):
    """
    Represents a order item by a customer in the system.
    """
    __tablename__ = "customer_order_item"

    order_id = Column(Integer, ForeignKey(
        'customer_order.order_id'
    ),primary_key=True, unique=True, index=True)
    item_id = Column(Integer, ForeignKey('product.product_id'))
    quantity = Column(Integer)
    

class Product(Base):
    """
    Represents a product in the system.
    """
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True, unique=True, index=True)
    