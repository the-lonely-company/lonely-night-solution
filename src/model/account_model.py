from pydantic import BaseModel
from typing import List, Optional
from datetime import date

from model.camel_model import CamelModel


class User(BaseModel):
    user_id: int
    email: str
    name: Optional[str] = None
    address: Optional[str] = None
    phone_number_prefix: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    is_merchant: Optional[bool] = False
    is_active: Optional[bool] = True

class Merchant(BaseModel):
    merchant_id: str
    email: str
    password: str
    address: Optional[str] = None
    delivery_fee: Optional[float] = None
    phone_number_prefix: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = True

class Transaction(BaseModel):
    reference_no: str
    status: str
    user_id: int
    merchant_id: int
    amount: float

class UserDetail(CamelModel):
    firebase_uid: str
    email: str
    name: str
