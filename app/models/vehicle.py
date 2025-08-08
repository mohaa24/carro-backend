from sqlalchemy import Integer, String, Float, Date, Enum, ForeignKey, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db import Base
import enum
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.user import User

class VehicleType(str, enum.Enum):
    car = "Car"
    motorbike = "Motor Bike"
    threeWheeler = "Three Wheeler"
    truck = "Truck"
    farm = "Farm"
    plant = "Plant"
    electricBike = "Electric Bike"
    van = "Van"
    other = "Other"

class FuelType(str, enum.Enum):
    petrol = "Petrol"
    diesel = "Diesel"
    electric = "Electric"
    hybrid = "Hybrid"

class TransmissionType(str, enum.Enum):
    manual = "Manual"
    automatic = "Automatic"

class SellerType(str, enum.Enum):
    dealer = "Dealer"
    private = "Private"

class ImportStatus(str, enum.Enum):
    used_import = "Used Import"
    new_import = "New Import"
    reconditioned = "Reconditioned"

class VehicleCondition(str, enum.Enum):
    used = "Used"
    new = "New"
    reconditioned = "Reconditioned"

class Vehicle(Base):
    __tablename__ = "vehicles"
    vehicle_type: Mapped[VehicleType] = mapped_column(Enum(VehicleType))
    images = relationship(
        "VehicleImage",
        back_populates="vehicle",
        cascade="all, delete-orphan"
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    posted_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(255))
    make: Mapped[str] = mapped_column(String(100))
    model: Mapped[str] = mapped_column(String(100))
    variant: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    year: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)  # Assume LKR
    mileage: Mapped[int] = mapped_column(Integer)  # In kilometers
    fuel_type: Mapped[FuelType] = mapped_column(Enum(FuelType))
    transmission: Mapped[TransmissionType] = mapped_column(Enum(TransmissionType))
    body_type: Mapped[str] = mapped_column(String(50))
    color: Mapped[str] = mapped_column(String(50))
    engine_size: Mapped[float] = mapped_column(Float)
    doors: Mapped[int] = mapped_column(Integer)
    registration_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)  # Registration/customs clearance date
    location: Mapped[str] = mapped_column(String(255))
    seller_type: Mapped[SellerType] = mapped_column(Enum(SellerType))
    import_status: Mapped[ImportStatus] = mapped_column(Enum(ImportStatus))
    condition: Mapped[VehicleCondition] = mapped_column(Enum(VehicleCondition))
    ownership_history: Mapped[int] = mapped_column(Integer)  # Number of previous owners
    description: Mapped[str] = mapped_column(String(1000))
    features: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)  # Vehicle features/amenities as array
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship to user who posted this vehicle
    posted_by = relationship("User", back_populates="vehicles")
