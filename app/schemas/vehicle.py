from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
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
    motorbike = "Motor Bike"
    threeWheeler = "Three Wheeler"
    truck = "Truck"
    farm = "Farm"
    plant = "Plant"
    electricBike = "Electric Bike"
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
    used = "Used"
    new = "New"
    reconditioned = "Reconditioned"


class VehicleImageOut(BaseModel):
    id: int
    url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class VehicleBase(BaseModel):
    vehicle_type: VehicleType
    description: str
    location: str
    title: str
    make: str
    model: str
    year: int
    price: float  # LKR
    mileage: int  # kilometers
    fuel_type: FuelType
    transmission: TransmissionType
    body_type: str
    condition: VehicleCondition
    ownership_history: int
    #Auto populated
    seller_type: SellerType
    #Optional
    variant: Optional[str] = None
    features: Optional[List[str]] = None
    color: Optional[str]
    engine_size: Optional[float] = None
    doors: Optional[int]
    insurance_expiry: Optional[date] = None
    import_status: Optional[ImportStatus]


class VehicleOut(VehicleBase):
    id: int
    posted_by_id: int
    created_at: datetime
    updated_at: datetime
    images: List[VehicleImageOut] = []

    class Config:
        from_attributes = True

class VehicleCreate(VehicleBase):
    images: Optional[List[VehicleImageCreate]] = []

# Import UserSummary with forward reference to avoid circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.schemas.user import UserSummary

class VehicleWithUser(VehicleOut):
    posted_by: "UserSummary"  # Include full user information

# At the end of the file, resolve forward references
from app.schemas.user import UserSummary
VehicleWithUser.model_rebuild()

