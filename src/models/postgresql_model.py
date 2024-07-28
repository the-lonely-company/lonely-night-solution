from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from connections.postgreSQL.postgresql_connection import Base

class Users(Base):
    """
    Represents a User in the system.
    """

    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, unique=True, index=True)
    firebase_uid = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    phone_number_prefix = Column(String)
    phone_number = Column(String, index=True)
    date_of_birth = Column(Date)
    is_merchant = Column(Boolean, default=False)

    customer_orders = relationship("Customer_Orders", back_populates="user")
    merchant = relationship("Merchants", back_populates="user", uselist=False)


class Merchants(Base):
    """
    Represents a merchant in the system.
    """
    __tablename__ = "Merchants"

    merchant_id = Column(Integer, primary_key=True, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    address = Column(String, index=True)
    delivery_fee = Column(Float)

    user_id = Column(Integer, ForeignKey('Users.user_id'), unique=True)

    user = relationship("Users", back_populates="merchant")
    customer_orders = relationship("Customer_Orders", back_populates="merchant")


class Customer_Orders(Base):
    """
    Represents a order by a customer in the system.
    """
    __tablename__ = "Customer_Orders"

    order_id = Column(Integer, primary_key=True, unique=True, index=True)
    reference_no = Column(Integer, unique=True, index=True)
    status = Column(String, index=True)
    date_order_placed = Column(Date)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    merchant_id = Column(Integer, ForeignKey('Merchants.merchant_id'))
    total_order_amount = Column(Float)

    user = relationship("Users", back_populates="customer_orders")
    merchant = relationship("Merchants", back_populates="customer_orders")

class Customer_Orders_Items(Base):
    """
    Represents a order item by a customer in the system.
    """
    __tablename__ = "Customer_Orders_Items"

    order_id = Column(Integer, ForeignKey(
        'Customer_Orders.order_id'
    ),primary_key=True, unique=True, index=True)
    item_id = Column(Integer, ForeignKey('Product.product_id'))
    quantity = Column(Integer)
    

class Product(Base):
    """
    Represents a product in the system.
    """
    __tablename__ = "Product"

    product_id = Column(Integer, primary_key=True, unique=True, index=True)
    