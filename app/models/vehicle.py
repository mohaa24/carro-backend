from sqlalchemy import Integer, String, Float, Date, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base
import enum
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

class VehicleType(str, enum.Enum):
    car = "Car"
    motorbike = "Motorbike"
    truck = "Truck"
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
    excellent = "Excellent"
    good = "Good"
    fair = "Fair"
    poor = "Poor"

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
    tax_due_date: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    insurance_expiry: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    location: Mapped[str] = mapped_column(String(255))
    seller_type: Mapped[SellerType] = mapped_column(Enum(SellerType))
    import_status: Mapped[ImportStatus] = mapped_column(Enum(ImportStatus))
    condition: Mapped[VehicleCondition] = mapped_column(Enum(VehicleCondition))
    ownership_history: Mapped[int] = mapped_column(Integer)  # Number of previous owners
    description: Mapped[str] = mapped_column(String(1000))
    vin: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Relationship to user who posted this vehicle
    posted_by = relationship("User", back_populates="vehicles")
