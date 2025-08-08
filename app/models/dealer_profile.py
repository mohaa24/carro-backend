from sqlalchemy import Integer, String, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db import Base
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.user import User

class DealerProfile(Base):
    __tablename__ = "dealer_profiles"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)  # One-to-one with User
    
    # Business identification
    business_id: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True)  # Custom business ID like "DEAL001"
    
    # Business details (some may duplicate User table for now, we'll clean up later)
    business_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Rich profile data
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    images: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)  # Array of image URLs
    rating: Mapped[float] = mapped_column(Float, default=0.0)  # 0-5 rating
    about_us: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)  # Long description
    favorites: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)  # Array of favorite items
    services: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)  # Array of services offered
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship back to user
    user = relationship("User", back_populates="dealer_profile")
