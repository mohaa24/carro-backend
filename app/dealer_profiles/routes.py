from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional

from app.db import async_session_maker
from app.models.dealer_profile import DealerProfile
from app.models.user import User, UserType
from app.schemas.dealer_profile import DealerProfileCreate, DealerProfileUpdate, DealerProfileOut
from app.auth import get_current_active_user

router = APIRouter(prefix="/api", tags=["dealer-profiles"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.post("/dealer-profile", response_model=DealerProfileOut)
async def create_dealer_profile(
    profile_data: DealerProfileCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a dealer profile (only for dealership users)."""
    
    # Check if user is a dealership
    if current_user.user_type != UserType.dealership:
        raise HTTPException(status_code=403, detail="Only dealership users can create dealer profiles")
    
    # Check if dealer profile already exists
    result = await db.execute(
        select(DealerProfile).where(DealerProfile.user_id == current_user.id)
    )
    existing_profile = result.scalar_one_or_none()
    
    if existing_profile:
        raise HTTPException(status_code=400, detail="Dealer profile already exists")
    
    # Create new dealer profile
    db_profile = DealerProfile(
        user_id=current_user.id,
        **profile_data.model_dump(exclude_unset=True)
    )
    
    db.add(db_profile)
    await db.commit()
    await db.refresh(db_profile)
    
    return db_profile

@router.get("/dealer-profile", response_model=DealerProfileOut)
async def get_my_dealer_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's dealer profile."""
    
    if current_user.user_type != UserType.dealership:
        raise HTTPException(status_code=403, detail="Only dealership users can access dealer profiles")
    
    result = await db.execute(
        select(DealerProfile).where(DealerProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Dealer profile not found")
    
    return profile

@router.get("/dealer-profile/{user_id}", response_model=DealerProfileOut)
async def get_dealer_profile_by_user_id(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get dealer profile by user ID (public access)."""
    
    result = await db.execute(
        select(DealerProfile).where(DealerProfile.user_id == user_id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Dealer profile not found")
    
    return profile

@router.put("/dealer-profile", response_model=DealerProfileOut)
async def update_dealer_profile(
    profile_data: DealerProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update current user's dealer profile."""
    
    if current_user.user_type != UserType.dealership:
        raise HTTPException(status_code=403, detail="Only dealership users can update dealer profiles")
    
    result = await db.execute(
        select(DealerProfile).where(DealerProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Dealer profile not found")
    
    # Update fields
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    await db.commit()
    await db.refresh(profile)
    
    return profile

@router.delete("/dealer-profile")
async def delete_dealer_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete current user's dealer profile."""
    
    if current_user.user_type != UserType.dealership:
        raise HTTPException(status_code=403, detail="Only dealership users can delete dealer profiles")
    
    result = await db.execute(
        select(DealerProfile).where(DealerProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Dealer profile not found")
    
    await db.delete(profile)
    await db.commit()
    
    return {"message": "Dealer profile deleted successfully"}
