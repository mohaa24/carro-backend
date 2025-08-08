from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DealerProfileBase(BaseModel):
    business_id: Optional[str] = None
    business_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    images: Optional[List[str]] = None
    rating: float = 0.0
    about_us: Optional[str] = None
    favorites: Optional[List[str]] = None
    services: Optional[List[str]] = None

class DealerProfileCreate(DealerProfileBase):
    pass  # All fields are optional for creation

class DealerProfileUpdate(BaseModel):
    business_id: Optional[str] = None
    business_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    images: Optional[List[str]] = None
    rating: Optional[float] = None
    about_us: Optional[str] = None
    favorites: Optional[List[str]] = None
    services: Optional[List[str]] = None

class DealerProfileOut(DealerProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# For including dealer profile in user responses
class DealerProfileSummary(BaseModel):
    id: int
    business_id: Optional[str] = None
    business_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    rating: float = 0.0
    
    class Config:
        from_attributes = True
