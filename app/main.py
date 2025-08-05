from fastapi import FastAPI
from app.vehicles.routes import router as vehicle_router
from app.users.routes import router as auth_router
# Import models to ensure they are registered with SQLAlchemy
from app.models import Vehicle, VehicleImage, User

app = FastAPI(title="Carro Backend API", description="Vehicle marketplace API with authentication")

@app.get("/")
def read_root():
    return {"message": "Hello from Carro backend!"}

app.include_router(vehicle_router)
app.include_router(auth_router)
