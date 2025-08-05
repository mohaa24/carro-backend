from pydantic import BaseModel, EmailStr
from typing import Optional
import enum

class UserType(str, enum.Enum):
    individual = "Individual"
    dealership = "Dealership"

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_type: UserType = UserType.individual
    business_name: Optional[str] = None
    business_registration: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_type: Optional[UserType] = None
    business_name: Optional[str] = None
    business_registration: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None

class UserRead(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class UserSummary(BaseModel):
    id: int
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_type: UserType
    business_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
