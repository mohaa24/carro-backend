#!/usr/bin/env python3
import os
import sys
import asyncio

async def init_database():
    """Initialize database tables"""
    try:
        print("🔧 Initializing database...")
        from app.db import engine, Base
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("✅ Database tables created/verified")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def seed_database():
    """Seed database with demo data if empty"""
    try:
        print("🌱 Checking if database needs seeding...")
        from seed_db import seed_database as run_seed
        await run_seed()
        print("✅ Database seeding completed!")
        return True
    except Exception as e:
        print(f"⚠️ Database seeding failed (continuing anyway): {e}")
        return False

def main():
    try:
        # Add current directory to Python path
        sys.path.insert(0, os.getcwd())
        
        # Get port from environment
        port = int(os.environ.get("PORT", 8000))
        print(f"🚀 Starting Carro Backend on port {port}...")
        print(f"📁 Working directory: {os.getcwd()}")
        print(f"🗄️  DATABASE_URL: {os.environ.get('DATABASE_URL', 'NOT SET')}")
        
        # Test import first
        print("📦 Testing import of app...")
        try:
            from app.main import app
            print("✅ App imported successfully!")
        except Exception as e:
            print(f"❌ Failed to import app: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        
        # Initialize database
        print("🔧 Initializing database...")
        if not asyncio.run(init_database()):
            print("❌ Database initialization failed, but continuing...")
        
        # Seed database with demo data (only if empty)
        print("🌱 Seeding database if needed...")
        asyncio.run(seed_database())
        
        # Import uvicorn after we know the app works
        print("📦 Importing uvicorn...")
        import uvicorn
        
        print(f"🌐 Starting uvicorn server on 0.0.0.0:{port}")
        print("🎉 Server ready! Check https://your-app.railway.app/docs for API documentation")
        
        # Use the imported app object directly instead of string path
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
        
    except Exception as e:
        print(f"💥 ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
