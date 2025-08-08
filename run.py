#!/usr/bin/env python3
import os
import sys

def main():
    try:
        # Get port from environment
        port = int(os.environ.get("PORT", 8000))
        print(f"Starting Carro Backend on port {port}...")
        
        # Basic imports to check if everything is working
        print("Importing modules...")
        import uvicorn
        
        print("Starting uvicorn...")
        # Use string module path to avoid import issues
        uvicorn.run("app.main:app", host="0.0.0.0", port=port, log_level="info")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
