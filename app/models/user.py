from sqlalchemy import String, Boolean, Integer, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db import Base
import enum
from typing import List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.vehicle import Vehicle
    from app.models.dealer_profile import DealerProfile

class UserType(str, enum.Enum):
    individual = "Individual"
    dealership = "Dealership"

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # User profile fields
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType), default=UserType.individual)
    
    # Dealership specific fields (only used if user_type is dealership)
    business_name: Mapped[str] = mapped_column(String(255), nullable=True)
    business_registration: Mapped[str] = mapped_column(String(100), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)  # Now required for all users
    address: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    vehicles = relationship("Vehicle", back_populates="posted_by")
    dealer_profile = relationship("DealerProfile", back_populates="user", uselist=False)  # One-to-one
