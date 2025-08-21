#!/usr/bin/env python3
"""
Flask Application Runner
This script starts the Flask portfolio application
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app

def main():
    """Main function to run the Flask app"""
    print("🚀 Starting Portfolio Application...")
    
    # Create Flask app
    app = create_app()
    
    # Get configuration
    debug = app.config.get('DEBUG', False)
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    print(f"📊 Configuration:")
    print(f"   - Debug Mode: {debug}")
    print(f"   - Host: {host}")
    print(f"   - Port: {port}")
    print(f"   - Database: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    
    print(f"\n🌐 Starting server at http://{host}:{port}")
    print("📝 Admin Panel: http://localhost:5000/admin/login")
    print("🔑 Login: admin / admin1234")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("Please check the error message above and try again.")

if __name__ == "__main__":
    main()
