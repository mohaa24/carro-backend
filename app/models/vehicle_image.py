from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db import Base
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.vehicle import Vehicle

class VehicleImage(Base):
    __tablename__ = "vehicle_images"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))
    url: Mapped[str] = mapped_column(String(500))
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    vehicle = relationship("Vehicle", back_populates="images")
