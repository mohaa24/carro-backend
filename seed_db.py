import asyncio
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select
from app.db import engine, Base
from app.models.vehicle import (
    Vehicle, FuelType, TransmissionType, SellerType,
    ImportStatus, VehicleCondition, VehicleType
)
from app.models.vehicle_image import VehicleImage
from app.models.user import User, UserType
from app.models.dealer_profile import DealerProfile
from app.auth import get_password_hash

async def seed_database():
    """Seed database with demo data only if it's empty"""
    print("🌱 Checking if database needs seeding...")
    
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        # Check if users already exist
        result = await session.execute(select(User))
        existing_users = result.scalars().all()
        
        if existing_users:
            print("✅ Database already has data, skipping seed")
            return
        
        print("🌱 Database is empty, adding demo data...")
        
        # Create demo users
        demo_users = [
            User(
                email="admin@carro.com",
                hashed_password=get_password_hash("admin123"),
                first_name="Admin",
                last_name="User",
                user_type=UserType.individual,
                phone="+94712345678",
                is_active=True,
                is_superuser=True,
                is_verified=True
            ),
            User(
                email="user@carro.com", 
                hashed_password=get_password_hash("user123"),
                first_name="Demo",
                last_name="User",
                user_type=UserType.individual,
                phone="+94723456789",
                is_active=True,
                is_superuser=False,
                is_verified=True
            ),
            User(
                email="dealer@carro.com",
                hashed_password=get_password_hash("dealer123"),
                first_name="John",
                last_name="Smith",
                user_type=UserType.dealership,
                business_name="Premium Auto Sales",
                business_registration="BR123456789",
                phone="+94771234567",
                address="123 Main Street, Colombo 03",
                is_active=True,
                is_superuser=False,
                is_verified=True
            )
        ]
        
        session.add_all(demo_users)
        await session.commit()
        
        # Get user IDs after commit
        user_individual = demo_users[1]  # Demo user
        user_dealer = demo_users[2]      # Dealer
        
        # Create dealer profile for the dealer user
        dealer_profile = DealerProfile(
            user_id=user_dealer.id,
            business_id="DEAL001",
            business_name="Premium Auto Sales",
            address="123 Main Street, Colombo 03",
            phone="+94771234567",
            website="https://premiumauto.lk",
            logo_url="https://via.placeholder.com/150x150/007bff/ffffff?text=PA",
            images=[
                "https://via.placeholder.com/800x600/007bff/ffffff?text=Showroom",
                "https://via.placeholder.com/800x600/28a745/ffffff?text=Office"
            ],
            rating=4.5,
            about_us="Premium Auto Sales has been serving Sri Lanka's automotive needs for over 15 years.",
            services=["Vehicle Sales", "Trade-ins", "Financing", "Insurance"],
            favorites=["Toyota", "Honda", "Nissan", "Mazda"]
        )
        
        session.add(dealer_profile)
        await session.commit()
        
        # Create demo vehicles
        vehicles = [
            Vehicle(
                posted_by_id=user_dealer.id,
                title="2017 Toyota Axio Hybrid",
                make="Toyota",
                model="Axio",
                variant="Hybrid G",
                year=2017,
                price=5400000,
                mileage=35000,
                fuel_type=FuelType.hybrid,
                transmission=TransmissionType.automatic,
                body_type="Sedan",
                color="White",
                engine_size=1.5,
                doors=4,
                registration_date=date(2017, 5, 20),
                location="Colombo",
                seller_type=SellerType.dealer,
                import_status=ImportStatus.used_import,
                condition=VehicleCondition.used,
                ownership_history=1,
                description="Reliable Toyota Axio Hybrid with excellent fuel economy.",
                features=["Air Conditioning", "Power Steering", "Electric Windows", "ABS", "Airbags"],
                vehicle_type=VehicleType.car,
                images=[
                    VehicleImage(url="https://www.onlycars.com.au/img/items/345483/01-l.jpg"),
                    VehicleImage(url="https://www.onlycars.com.au/img/items/345483/02-l.jpg"),
                ]
            ),
            Vehicle(
                posted_by_id=user_individual.id,
                title="2019 Honda CB125F",
                make="Honda",
                model="CB125F",
                year=2019,
                price=670000,
                mileage=8000,
                fuel_type=FuelType.petrol,
                transmission=TransmissionType.manual,
                body_type="Motorbike",
                color="Matte Black",
                engine_size=0.125,
                doors=0,
                registration_date=date(2019, 3, 15),
                location="Kandy",
                seller_type=SellerType.private,
                import_status=ImportStatus.new_import,
                condition=VehicleCondition.new,
                ownership_history=1,
                description="Lightweight and fuel-efficient Honda CB125F.",
                features=["Electric Start", "LED Headlight", "Digital Display"],
                vehicle_type=VehicleType.motorbike,
                images=[
                    VehicleImage(url="https://bikes.motobank.co.uk/fp/30510/honda-cbf125-na-j-2019-red_399028.jpg"),
                ]
            ),
            Vehicle(
                posted_by_id=user_dealer.id,
                title="2015 Nissan X-Trail",
                make="Nissan",
                model="X-Trail",
                variant="ST",
                year=2015,
                price=5800000,
                mileage=65000,
                fuel_type=FuelType.diesel,
                transmission=TransmissionType.automatic,
                body_type="SUV",
                color="Silver",
                engine_size=2.0,
                doors=5,
                registration_date=date(2015, 9, 10),
                location="Galle",
                seller_type=SellerType.dealer,
                import_status=ImportStatus.used_import,
                condition=VehicleCondition.used,
                ownership_history=2,
                description="Well-maintained Nissan X-Trail SUV with spacious interior.",
                features=["4WD", "Air Conditioning", "ABS", "Multiple Airbags", "Bluetooth"],
                vehicle_type=VehicleType.car,
                images=[
                    VehicleImage(url="https://images.clickdealer.co.uk/vehicles/5813/5813649/large1/136980230.jpg"),
                ]
            ),
        ]

        session.add_all(vehicles)
        await session.commit()
        
        print(f"✅ Database seeded with {len(vehicles)} vehicles and {len(demo_users)} users!")
        print("Demo accounts:")
        print("  - admin@carro.com / admin123 (admin)")
        print("  - user@carro.com / user123 (regular user)")
        print("  - dealer@carro.com / dealer123 (dealership with profile)")

async def init_tables():
    """Initialize database tables without dropping existing ones"""
    print("🔧 Initializing database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables ready")

if __name__ == "__main__":
    print("Running database seeding script...")
    asyncio.run(seed_database())
    print("Script completed!")
