# Import all models to ensure they are registered with SQLAlchemy
from .vehicle import Vehicle
from .vehicle_image import VehicleImage
from .user import User

__all__ = ["Vehicle", "VehicleImage", "User"]
