from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from typing import Optional

from app.db import async_session_maker
from app.models.vehicle import Vehicle, FuelType, TransmissionType, VehicleCondition, SellerType
from app.models.user import User
from app.schemas.vehicle import VehicleOut, VehicleCreate, VehicleWithUser
from app.auth import get_current_active_user

router = APIRouter(prefix="/api", tags=["vehicles"])

async def get_db():
    async with async_session_maker() as session:
        yield session

def build_vehicle_search_query(
    make: Optional[str] = None,
    model: Optional[str] = None,
    location: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    fuel_type: Optional[str] = None,
    transmission: Optional[str] = None,
    body_type: Optional[str] = None,
    condition: Optional[str] = None,
    seller_type: Optional[str] = None,
    vehicle_type: Optional[str] = None,
):
    """Build a filtered query for vehicle search"""
    query = select(Vehicle).options(
        selectinload(Vehicle.images),
        selectinload(Vehicle.posted_by).selectinload(User.dealer_profile)
    )
    
    filters = []
    
    if make:
        filters.append(Vehicle.make.ilike(f"%{make}%"))
    if model:
        filters.append(Vehicle.model.ilike(f"%{model}%"))
    if location:
        filters.append(Vehicle.location.ilike(f"%{location}%"))
    if min_price is not None:
        filters.append(Vehicle.price >= min_price)
    if max_price is not None:
        filters.append(Vehicle.price <= max_price)
    if min_year is not None:
        filters.append(Vehicle.year >= min_year)
    if max_year is not None:
        filters.append(Vehicle.year <= max_year)
    if fuel_type:
        filters.append(Vehicle.fuel_type == fuel_type)
    if transmission:
        filters.append(Vehicle.transmission == transmission)
    if body_type:
        filters.append(Vehicle.body_type.ilike(f"%{body_type}%"))
    if condition:
        filters.append(Vehicle.condition == condition)
    if seller_type:
        filters.append(Vehicle.seller_type == seller_type)
    if vehicle_type:
        filters.append(Vehicle.vehicle_type == vehicle_type)
    
    if filters:
        query = query.where(and_(*filters))
    
    return query

@router.get("/vehicles", response_model=list[VehicleOut])
async def get_vehicles(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    make: Optional[str] = Query(None, description="Filter by vehicle make"),
    model: Optional[str] = Query(None, description="Filter by vehicle model"),
    location: Optional[str] = Query(None, description="Filter by location"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    min_year: Optional[int] = Query(None, ge=1900, description="Minimum year filter"),
    max_year: Optional[int] = Query(None, le=2030, description="Maximum year filter"),
    fuel_type: Optional[str] = Query(None, description="Filter by fuel type (petrol, diesel, electric, hybrid)"),
    transmission: Optional[str] = Query(None, description="Filter by transmission (manual, automatic)"),
    body_type: Optional[str] = Query(None, description="Filter by body type"),
    condition: Optional[str] = Query(None, description="Filter by condition (used, new, reconditioned)"),
    seller_type: Optional[str] = Query(None, description="Filter by seller type (dealer, private)"),
    vehicle_type: Optional[str] = Query(None, description="Filter by vehicle type (car, motorbike, truck, etc.)"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get vehicles with search filters (requires authentication)."""
    offset = (page - 1) * limit
    
    query = build_vehicle_search_query(
        make=make,
        model=model,
        location=location,
        min_price=min_price,
        max_price=max_price,
        min_year=min_year,
        max_year=max_year,
        fuel_type=fuel_type,
        transmission=transmission,
        body_type=body_type,
        condition=condition,
        seller_type=seller_type,
        vehicle_type=vehicle_type,
    )
    
    result = await db.execute(query.offset(offset).limit(limit))
    vehicles = result.scalars().unique().all()
    return vehicles

# Public endpoint for unauthenticated access (if needed)
@router.get("/vehicles/public", response_model=list[VehicleOut])
async def get_vehicles_public(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    make: Optional[str] = Query(None, description="Filter by vehicle make"),
    model: Optional[str] = Query(None, description="Filter by vehicle model"),
    location: Optional[str] = Query(None, description="Filter by location"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    min_year: Optional[int] = Query(None, ge=1900, description="Minimum year filter"),
    max_year: Optional[int] = Query(None, le=2030, description="Maximum year filter"),
    fuel_type: Optional[str] = Query(None, description="Filter by fuel type (petrol, diesel, electric, hybrid)"),
    transmission: Optional[str] = Query(None, description="Filter by transmission (manual, automatic)"),
    body_type: Optional[str] = Query(None, description="Filter by body type"),
    condition: Optional[str] = Query(None, description="Filter by condition (used, new, reconditioned)"),
    seller_type: Optional[str] = Query(None, description="Filter by seller type (dealer, private)"),
    vehicle_type: Optional[str] = Query(None, description="Filter by vehicle type (car, motorbike, truck, etc.)"),
    db: AsyncSession = Depends(get_db),
):
    """Get vehicles with search filters (public access)."""
    offset = (page - 1) * limit
    
    query = build_vehicle_search_query(
        make=make,
        model=model,
        location=location,
        min_price=min_price,
        max_price=max_price,
        min_year=min_year,
        max_year=max_year,
        fuel_type=fuel_type,
        transmission=transmission,
        body_type=body_type,
        condition=condition,
        seller_type=seller_type,
        vehicle_type=vehicle_type,
    )
    
    result = await db.execute(query.offset(offset).limit(limit))
    vehicles = result.scalars().unique().all()
    return vehicles

@router.get("/vehicles/{vehicle_id}", response_model=VehicleWithUser)
async def get_vehicle_by_id(
    vehicle_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific vehicle by ID (public access)."""
    query = select(Vehicle).options(
        selectinload(Vehicle.images),
        selectinload(Vehicle.posted_by).selectinload(User.dealer_profile)
    ).where(Vehicle.id == vehicle_id)
    
    result = await db.execute(query)
    vehicle = result.scalar_one_or_none()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    return vehicle

@router.post("/vehicles", response_model=VehicleOut)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new vehicle listing (requires authentication)."""
    from app.models.vehicle_image import VehicleImage
    
    # Create the vehicle
    db_vehicle = Vehicle(
        posted_by_id=current_user.id,
        vehicle_type=vehicle_data.vehicle_type,
        title=vehicle_data.title,
        make=vehicle_data.make,
        model=vehicle_data.model,
        variant=vehicle_data.variant,
        year=vehicle_data.year,
        price=vehicle_data.price,
        mileage=vehicle_data.mileage,
        fuel_type=vehicle_data.fuel_type,
        transmission=vehicle_data.transmission,
        body_type=vehicle_data.body_type,
        color=vehicle_data.color,
        engine_size=vehicle_data.engine_size,
        doors=vehicle_data.doors,
        location=vehicle_data.location,
        seller_type=vehicle_data.seller_type,
        import_status=vehicle_data.import_status,
        condition=vehicle_data.condition,
        ownership_history=vehicle_data.ownership_history,
        description=vehicle_data.description,
    )
    
    # Add images if provided
    if vehicle_data.images:
        for image_data in vehicle_data.images:
            db_image = VehicleImage(url=image_data.url)
            db_vehicle.images.append(db_image)
    
    db.add(db_vehicle)
    await db.commit()
    await db.refresh(db_vehicle)
    
    # Fetch with relationships
    result = await db.execute(
        select(Vehicle)
        .options(
            selectinload(Vehicle.images),
            selectinload(Vehicle.posted_by)
        )
        .where(Vehicle.id == db_vehicle.id)
    )
    created_vehicle = result.scalar_one()
    
    return created_vehicle
