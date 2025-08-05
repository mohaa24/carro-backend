from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey
from app.db import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.vehicle import Vehicle

class VehicleImage(Base):
    __tablename__ = "vehicle_images"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))
    url: Mapped[str] = mapped_column(String(500))

    vehicle = relationship("Vehicle", back_populates="images")
