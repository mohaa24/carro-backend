from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db import async_session_maker
from app.models.vehicle import Vehicle
from app.models.user import User
from app.schemas.vehicle import VehicleOut, VehicleCreate
from app.auth import get_current_active_user

router = APIRouter(prefix="/api", tags=["vehicles"])

async def get_db():
    async with async_session_maker() as session:
        yield session

@router.get("/vehicles", response_model=list[VehicleOut])
async def get_vehicles(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all vehicles (requires authentication)."""
    offset = (page - 1) * limit
    result = await db.execute(
        select(Vehicle)
        .options(
            selectinload(Vehicle.images),
            selectinload(Vehicle.posted_by)
        )
        .offset(offset)
        .limit(limit)
    )
    vehicles = result.scalars().unique().all()
    return vehicles

# Public endpoint for unauthenticated access (if needed)
@router.get("/vehicles/public", response_model=list[VehicleOut])
async def get_vehicles_public(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db),
):
    """Get all vehicles (public access)."""
    offset = (page - 1) * limit
    result = await db.execute(
        select(Vehicle)
        .options(
            selectinload(Vehicle.images),
            selectinload(Vehicle.posted_by)
        )
        .offset(offset)
        .limit(limit)
    )
    vehicles = result.scalars().unique().all()
    return vehicles

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
        registration_date=vehicle_data.registration_date,
        tax_due_date=vehicle_data.tax_due_date,
        insurance_expiry=vehicle_data.insurance_expiry,
        location=vehicle_data.location,
        seller_type=vehicle_data.seller_type,
        import_status=vehicle_data.import_status,
        condition=vehicle_data.condition,
        ownership_history=vehicle_data.ownership_history,
        description=vehicle_data.description,
        vin=vehicle_data.vin
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
