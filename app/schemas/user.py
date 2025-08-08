from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import enum

# Import DealerProfileSummary with forward reference to avoid circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.schemas.dealer_profile import DealerProfileSummary

class UserType(str, enum.Enum):
    individual = "Individual"
    dealership = "Dealership"

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_type: UserType = UserType.individual
    phone: str  # Now required for all users
    
    # Dealership specific fields (only used if user_type is dealership)
    business_name: Optional[str] = None
    business_registration: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None  # New dealer field
    
    # Common fields
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

class UserCreate(UserBase):
    password: str

class DealerRegistrationData(BaseModel):
    """Extended dealer profile data for registration"""
    business_id: Optional[str] = None
    logo_url: Optional[str] = None
    images: Optional[List[str]] = None
    rating: float = 0.0
    about_us: Optional[str] = None
    favorites: Optional[List[str]] = None
    services: Optional[List[str]] = None

class UserCreateWithDealer(UserCreate):
    """User registration schema that includes optional dealer profile data"""
    dealer_profile: Optional[DealerRegistrationData] = None

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
    created_at: datetime
    updated_at: datetime
    dealer_profile: Optional["DealerProfileSummary"] = None  # Include dealer profile if user is a dealer
    
    class Config:
        from_attributes = True

class UserSummary(BaseModel):
    id: int
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_type: UserType
    phone: str  # Now required for all users
    business_name: Optional[str] = None
    dealer_profile: Optional["DealerProfileSummary"] = None  # Include dealer profile summary
    
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

# At the end of the file, update forward references
from app.schemas.dealer_profile import DealerProfileSummary
UserRead.model_rebuild()
UserSummary.model_rebuild()
