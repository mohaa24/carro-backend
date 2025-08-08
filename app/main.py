from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.vehicles.routes import router as vehicle_router
from app.users.routes import router as auth_router
from app.dealer_profiles.routes import router as dealer_profile_router
# Import models to ensure they are registered with SQLAlchemy
from app.models import Vehicle, VehicleImage, User
from app.models.dealer_profile import DealerProfile

app = FastAPI(title="Carro Backend API", description="Vehicle marketplace API with authentication")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"message": "Hello from Carro backend!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "carro-backend"}

app.include_router(vehicle_router)
app.include_router(auth_router)
app.include_router(dealer_profile_router)
