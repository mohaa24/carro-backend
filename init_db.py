import asyncio
from datetime import date
from app.db import engine, Base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.models.vehicle import (
    Vehicle, FuelType, TransmissionType, SellerType,
    ImportStatus, VehicleCondition, VehicleType
)
from app.models.vehicle_image import VehicleImage
from app.models.user import User, UserType
from app.models.dealer_profile import DealerProfile
from app.auth import get_password_hash

async def create_tables_and_seed():
    print("Starting database initialization...")
    
    async with engine.begin() as conn:
        print("Dropping existing tables...")
        await conn.run_sync(Base.metadata.drop_all)  # WARNING: Drops all tables, use carefully
        print("Creating new tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully!")

    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        print("Adding vehicles to database...")
        
        # First create and commit users
        demo_users = [
            User(
                email="admin@carro.com",
                hashed_password=get_password_hash("admin123"),
                first_name="Admin",
                last_name="User",
                user_type=UserType.individual,
                phone="+94712345678",  # Added phone number
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
                phone="+94723456789",  # Added phone number
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
                "https://via.placeholder.com/800x600/28a745/ffffff?text=Office",
                "https://via.placeholder.com/800x600/dc3545/ffffff?text=Workshop"
            ],
            rating=4.5,
            about_us="Premium Auto Sales has been serving Sri Lanka's automotive needs for over 15 years. We specialize in high-quality used and reconditioned vehicles, offering comprehensive warranties and excellent after-sales service.",
            services=["Vehicle Sales", "Trade-ins", "Financing", "Insurance", "Extended Warranty", "After-sales Service"],
            favorites=["Toyota", "Honda", "Nissan", "Mazda"]
        )
        
        session.add(dealer_profile)
        await session.commit()
        
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
                features=["Air Conditioning", "Power Steering", "Electric Windows", "Alloy Wheels", "ABS", "Airbags", "Bluetooth", "USB", "Navigation System"],
                vehicle_type=VehicleType.car,
                images=[
                    VehicleImage(url="https://www.onlycars.com.au/img/items/345483/01-l.jpg"),
                    VehicleImage(url="https://www.onlycars.com.au/img/items/345483/02-l.jpg"),
                    VehicleImage(url="https://www.onlycars.com.au/img/items/345483/05-l.jpg"),

                ]
            ),
            Vehicle(
                posted_by_id=user_individual.id,
                title="2019 Honda CB125F",
                make="Honda",
                model="CB125F",
                variant=None,
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
                description="Lightweight and fuel-efficient Honda CB125F, perfect for city commuting.",
                features=["Electric Start", "LED Headlight", "Digital Display", "Front Disc Brake", "Fuel Efficient Engine"],
                vehicle_type=VehicleType.motorbike,
                images=[
                    VehicleImage(url="https://bikes.motobank.co.uk/fp/30510/honda-cbf125-na-j-2019-red_399028.jpg"),
                    VehicleImage(url="https://bikes.motobank.co.uk/fp/30510/honda-cbf125-na-j-2019-red_399040.jpg"),
                    VehicleImage(url="https://bikes.motobank.co.uk/fp/30510/honda-cbf125-na-j-2019-red_399039.jpg"),
                    VehicleImage(url="https://bikes.motobank.co.uk/fp/30510/honda-cbf125-na-j-2019-red_399031.jpg"),

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
                description="Well-maintained Nissan X-Trail SUV with spacious interior and strong performance.",
                features=["4WD", "Air Conditioning", "Power Steering", "Cruise Control", "Alloy Wheels", "ABS", "Multiple Airbags", "Bluetooth", "Reverse Camera", "Roof Rails"],
                vehicle_type=VehicleType.car,
                images=[
                    VehicleImage(url="https://images.clickdealer.co.uk/vehicles/5813/5813649/large1/136980230.jpg"),
                    VehicleImage(url="https://images.clickdealer.co.uk/vehicles/5813/5813649/large1/136980229.jpg"),
                    VehicleImage(url="https://images.clickdealer.co.uk/vehicles/5813/5813649/large1/136980238.jpg"),
                    VehicleImage(url="https://images.clickdealer.co.uk/vehicles/5813/5813649/large1/136980239.jpg"),

                ]
            ),
            Vehicle(
                posted_by_id=user_individual.id,
                title="2021 Suzuki GSX-R150",
                make="Suzuki",
                model="GSX-R150",
                variant=None,
                year=2021,
                price=1700000,
                mileage=3000,
                fuel_type=FuelType.petrol,
                transmission=TransmissionType.manual,
                body_type="Motorbike",
                color="Blue",
                engine_size=0.147,
                doors=0,
                registration_date=date(2021, 1, 25),
                location="Negombo",
                seller_type=SellerType.private,
                import_status=ImportStatus.new_import,
                condition=VehicleCondition.new,
                ownership_history=1,
                description="Sporty Suzuki GSX-R150 with agile handling and great fuel efficiency.",
                features=["Liquid Cooled Engine", "Electric Start", "LED Headlight", "Digital Display", "Front & Rear Disc Brakes", "Racing Style"],
                vehicle_type=VehicleType.motorbike,
                images=[
                    VehicleImage(url="https://bikes.motobank.co.uk/fp/57620/suzuki-gsxr125-rlz-m1-2021-silver_885325.jpg"),
                    VehicleImage(url="https://bikes.motobank.co.uk/fp/57620/suzuki-gsxr125-rlz-m1-2021-silver_884552.jpg"),
                    VehicleImage(url="https://bikes.motobank.co.uk/fp/57620/suzuki-gsxr125-rlz-m1-2021-silver_884554.jpg"),
                    VehicleImage(url="https://bikes.motobank.co.uk/fp/57620/suzuki-gsxr125-rlz-m1-2021-silver_884557.jpg"),
                ]
            ),
            Vehicle(
                posted_by_id=user_dealer.id,
                title="2016 Mazda CX-5",
                make="Mazda",
                model="CX-5",
                variant="Sport",
                year=2016,
                price=6500000,
                mileage=52000,
                fuel_type=FuelType.petrol,
                transmission=TransmissionType.automatic,
                body_type="SUV",
                color="Red",
                engine_size=2.0,
                doors=5,
                registration_date=date(2016, 7, 5),
                location="Colombo",
                seller_type=SellerType.dealer,
                import_status=ImportStatus.used_import,
                condition=VehicleCondition.used,
                ownership_history=1,
                description="Mazda CX-5 with sporty handling and sleek design, perfect for families.",
                features=["AWD", "Sunroof", "Leather Seats", "Heated Seats", "BOSE Sound System", "Blind Spot Monitoring", "Lane Departure Warning", "Smart Key"],
                vehicle_type=VehicleType.car,
                images=[
                    VehicleImage(url="https://m.atcdn.co.uk/a/media/w1024/7551ab0d7d454f12a9a8002a1f10a193.jpg"),
                    VehicleImage(url="https://m.atcdn.co.uk/a/media/w1024/113296c92e83442c99f0469dd3bcfa19.jpg"),
                    VehicleImage(url="https://m.atcdn.co.uk/a/media/w1024/d0a588fb44264e818076d5eea461d8e4.jpg"),
                    VehicleImage(url="https://m.atcdn.co.uk/a/media/w1024/0975fce56cd446a8a58ef7cc0060858a.jpg"),
                ]
            ),
            Vehicle(
                posted_by_id=user_dealer.id,
                title="2018 Mitsubishi Lancer",
                make="Mitsubishi",
                model="Lancer",
                variant="GT",
                year=2018,
                price=4200000,
                mileage=40000,
                fuel_type=FuelType.petrol,
                transmission=TransmissionType.automatic,
                body_type="Sedan",
                color="Black",
                engine_size=1.8,
                doors=4,
                registration_date=date(2018, 8, 30),
                location="Matara",
                seller_type=SellerType.dealer,
                import_status=ImportStatus.used_import,
                condition=VehicleCondition.used,
                ownership_history=1,
                description="Sporty Mitsubishi Lancer GT with great performance and comfort.",
                features=["Turbo Engine", "Sports Suspension", "Racing Seats", "Spoiler", "Alloy Wheels", "Push Button Start", "Premium Sound System"],
                vehicle_type=VehicleType.car,
                images=[
                    VehicleImage(url="https://m.atcdn.co.uk/a/media/w1024/b7ca99dad7654eda9aa3220d79e65c06.jpg"),
                    VehicleImage(url="https://cdn.carsguide.com.au/cars/mitsubishi/lancer-2018-12596714-2.jpg"),
                    VehicleImage(url="https://m.atcdn.co.uk/a/media/w1024/92be34b08cf94877a1bd788e1937b90e.jpg"),
                    VehicleImage(url="https://m.atcdn.co.uk/a/media/w1024/465af8d95a15486ca3228aab12903575.jpg"),
                ]
            ),
        ]

        session.add_all(vehicles)
        print("Committing changes...")
        await session.commit()
        print("Database seeded with 6 vehicles, 3 demo users, and 1 dealer profile!")
        print("Demo users:")
        print("  - admin@carro.com / admin123 (admin)")
        print("  - user@carro.com / user123 (regular user)")
        print("  - dealer@carro.com / dealer123 (dealership with profile)")

if __name__ == "__main__":
    print("Running database initialization script...")
    asyncio.run(create_tables_and_seed())
    print("Script completed!")
