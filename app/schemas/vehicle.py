from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import enum

# Import UserSummary - using forward reference to avoid circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.schemas.user import UserSummary

class VehicleImageCreate(BaseModel):
    url: str

class FuelType(str, enum.Enum):
    petrol = "Petrol"
    diesel = "Diesel"
    electric = "Electric"
    hybrid = "Hybrid"

class VehicleType(str, enum.Enum):
    car = "Car"
    motorbike = "Motorbike"
    truck = "Truck"
    van = "Van"
    other = "Other"

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

class VehicleImageOut(BaseModel):
    id: int
    url: str

    class Config:
        from_attributes = True

class VehicleBase(BaseModel):
    vehicle_type: VehicleType
    title: str
    make: str
    model: str
    variant: Optional[str] = None
    year: int
    price: float  # LKR
    mileage: int  # kilometers
    fuel_type: FuelType
    transmission: TransmissionType
    body_type: str
    color: str
    engine_size: float
    doors: int
    registration_date: Optional[date] = None
    tax_due_date: Optional[date] = None
    insurance_expiry: Optional[date] = None
    location: str
    seller_type: SellerType
    import_status: ImportStatus
    condition: VehicleCondition
    ownership_history: int
    description: str
    vin: Optional[str] = None

class VehicleOut(VehicleBase):
    id: int
    posted_by_id: int
    images: List[VehicleImageOut] = []

    class Config:
        from_attributes = True

class VehicleCreate(VehicleBase):
    images: Optional[List[VehicleImageCreate]] = []

# Define this after importing UserSummary to avoid circular imports
class VehicleWithUser(VehicleOut):
    pass  # Will be updated after UserSummary is available

