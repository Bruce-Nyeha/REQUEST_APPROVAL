from pydantic import BaseModel, EmailStr
from datetime import datetime
from enums import UserRole

"""Request and Response data. This is the user registeratation request and response and the login response and request."""
class UserBase(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    

class UserCreate(UserBase):
    password: str
    role: UserRole   

class UserResponse(BaseModel):
    id: str 
    full_name: str
    username: str
    email: EmailStr
    role: UserRole 
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer" 


    