from pydantic import BaseModel
from typing import Optional

class schema_user(BaseModel):
    name: str
    email: str
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