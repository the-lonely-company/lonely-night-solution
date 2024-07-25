from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from connections.postgreSQL.postgresql_connection import Base

class User(Base):
    """
    Represents a User in the system.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    phone_number_prefix = Column(String)
    phone_number = Column(String, index=True)
    birthday = Column(Date)
    is_active = Column(Boolean, default=True)
    
    transactions = relationship("Transaction", back_populates="user")


class Merchant(Base):
    """
    Represents a merchant in the system.
    """
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True)
    merchant_id = Column(Integer, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    address = Column(String, index=True)
    delivery_fee = Column(Float)
    phone_number_prefix = Column(String)
    phone_number = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    
    transactions = relationship("Transaction", back_populates="merchant")


class Transaction(Base):
    """
    Represents a transaction in the system.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    reference_no = Column(Integer, unique=True, index=True)
    status = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    merchant_id = Column(Integer, ForeignKey('merchants.merchant_id'))
    amount = Column(Float)

    user = relationship("User", back_populates="transactions")
    merchant = relationship("Merchant", back_populates="transactions")