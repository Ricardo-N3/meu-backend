from pydantic import BaseModel, EmailStr
from typing import Optional

class schema_user(BaseModel):
    name: str
    email: EmailStr
    passwords: str
    active: Optional [bool]
    admin: Optional [bool]
    
    class Config:
        from_attributes = True

class SchemaOrder(BaseModel):
    users_id: int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    passwords: str

    class Config:
        from_attributes = True

class OrderItemSchema(BaseModel):
    quantity: int
    flavor: str
    size: str
    unitary_cost: float

    class Config:
        from_attributes = True

class ResponseOrderSchema(BaseModel):
    id: int
    status: str
    cost: float
    itens: list[OrderItemSchema]

    class Config:
        from_attributes = True