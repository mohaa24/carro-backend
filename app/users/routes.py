from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.auth import (
    authenticate_user, create_access_token, get_password_hash,
    get_current_active_user, get_db, ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.models.user import User
from app.models.dealer_profile import DealerProfile
from app.schemas.user import UserCreate, UserRead, UserLogin, Token, UserCreateWithDealer

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserRead)
async def register(user_data: UserCreateWithDealer, db: AsyncSession = Depends(get_db)):
    """Register a new user with optional dealer profile."""
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        user_type=user_data.user_type,
        business_name=user_data.business_name,
        business_registration=user_data.business_registration,
        phone=user_data.phone,
        address=user_data.address,
        is_active=user_data.is_active,
        is_superuser=user_data.is_superuser,
        is_verified=user_data.is_verified
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    # If user is a dealership and dealer profile data is provided, create dealer profile
    if user_data.user_type.value == "Dealership" and user_data.dealer_profile:
        dealer_data = user_data.dealer_profile
        db_dealer_profile = DealerProfile(
            user_id=db_user.id,
            business_id=dealer_data.business_id,
            business_name=user_data.business_name,  # Use business_name from user data
            address=user_data.address,  # Use address from user data
            phone=user_data.phone,  # Use phone from user data
            website=user_data.website if hasattr(user_data, 'website') else None,  # Use website from user data if available
            logo_url=dealer_data.logo_url,
            images=dealer_data.images,
            rating=dealer_data.rating,
            about_us=dealer_data.about_us,
            favorites=dealer_data.favorites,
            services=dealer_data.services
        )
        
        db.add(db_dealer_profile)
        await db.commit()
        await db.refresh(db_dealer_profile)
    
    # Re-fetch the user with dealer profile to ensure proper loading
    result = await db.execute(
        select(User).options(selectinload(User.dealer_profile)).where(User.id == db_user.id)
    )
    db_user = result.scalar_one()
    
    return db_user

@router.post("/register-simple", response_model=UserRead)
async def register_simple(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user (simple registration without dealer profile)."""
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        user_type=user_data.user_type,
        business_name=user_data.business_name,
        business_registration=user_data.business_registration,
        phone=user_data.phone,
        address=user_data.address,
        is_active=user_data.is_active,
        is_superuser=user_data.is_superuser,
        is_verified=user_data.is_verified
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    # Re-fetch the user with dealer profile to ensure proper loading
    result = await db.execute(
        select(User).options(selectinload(User.dealer_profile)).where(User.id == db_user.id)
    )
    db_user = result.scalar_one()
    
    return db_user

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login and get access token."""
    user = await authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Login with OAuth2 form and get access token (for OpenAPI docs)."""
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user information."""
    # Re-fetch the user with dealer profile to ensure proper loading
    result = await db.execute(
        select(User).options(selectinload(User.dealer_profile)).where(User.id == current_user.id)
    )
    user_with_profile = result.scalar_one()
    
    return user_with_profile
