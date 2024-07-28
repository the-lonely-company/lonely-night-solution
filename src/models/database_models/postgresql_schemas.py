from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class UserBase(BaseModel):
    user_id: int
    firebase_uid: str
    email: str
    name: Optional[str] = None
    address: Optional[str] = None
    phone_number_prefix: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    is_merchant: Optional[bool] = False
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    pass

class User(UserBase):
    transactions: List['Transaction'] = []

    class Config:
        orm_mode = True

class MerchantBase(BaseModel):
    merchant_id: str
    email: str
    password: str
    address: Optional[str] = None
    delivery_fee: Optional[float] = None
    phone_number_prefix: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = True

class MerchantCreate(MerchantBase):
    pass

class Merchant(MerchantBase):
    id: int
    transactions: List['Transaction'] = []

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    reference_no: str
    status: str
    user_id: int
    merchant_id: int
    amount: float

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    user: User
    merchant: Merchant

    class Config:
        orm_mode = True