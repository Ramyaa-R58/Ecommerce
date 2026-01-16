from typing import List, Optional

from pydantic import BaseModel

class LoginDetails(BaseModel):
    email: str
    password: str
class UserRoleData(BaseModel):
    user_id:int
    role_name:str
class UserDetails(LoginDetails):
    full_name:str
    phone_number:str

class AddressDetails(BaseModel):
    address_line1: str
    address_line2: str | None = None

class CategoryDetails(BaseModel):
    category_id:Optional[int] = None
    category_name: str
    category_description: str | None = None
class ProductDetails(BaseModel):
    product_name: str
    product_description: str | None = None
    price: float
    stock_quantity: int
    specifications: dict | None = None
    category_id: int

class CartProductDetails(BaseModel):
    product_id: int
    quantity: int
class PaymentDetails(BaseModel):
    payment_status:str
    order_id:int






