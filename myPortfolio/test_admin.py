#!/usr/bin/env python3
"""
Admin Panel Test Script
This script tests the admin panel functionality
"""

import requests
import os
from urllib.parse import urljoin

# Configuration
BASE_URL = "http://localhost:5000"
ADMIN_CREDENTIALS = {
    "username": "admin",
    "password": "admin1234"
}

def test_admin_login():
    """Test admin login functionality"""
    print("🔐 Testing Admin Panel Access...")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"✅ Server Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Please start your Flask app first.")
        return False
    except Exception as e:
        print(f"❌ Server error: {e}")
        return False
    
    # Test 2: Access login page
    try:
        login_url = urljoin(BASE_URL, "/login")
        response = requests.get(login_url)
        if response.status_code == 200:
            print("✅ Login page accessible")
        else:
            print(f"❌ Login page error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Login page error: {e}")
        return False
    
    # Test 3: Test login with credentials
    try:
        login_data = {
            "username": ADMIN_CREDENTIALS["username"],
            "password": ADMIN_CREDENTIALS["password"]
        }
        
        session = requests.Session()
        response = session.post(login_url, data=login_data, allow_redirects=False)
        
        if response.status_code == 302:  # Redirect after successful login
            print("✅ Login successful - credentials working")
            
            # Test 4: Access admin dashboard
            dashboard_url = urljoin(BASE_URL, "/admin/")
            response = session.get(dashboard_url)
            
            if response.status_code == 200:
                print("✅ Admin dashboard accessible")
                print("✅ Admin panel is fully functional!")
            else:
                print(f"❌ Dashboard access error: {response.status_code}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print("Check your ADMIN_USERNAME and ADMIN_PASSWORD in .env file")
            return False
            
    except Exception as e:
        print(f"❌ Login test error: {e}")
        return False
    
    return True

def show_admin_urls():
    """Display all admin panel URLs"""
    print("\n🌐 Admin Panel URLs:")
    print("=" * 50)
    print(f"Login: {BASE_URL}/login")
    print(f"Dashboard: {BASE_URL}/admin/")
    print(f"Projects: {BASE_URL}/admin/projects")
    print(f"Skills: {BASE_URL}/admin/skills")
    print(f"Blogs: {BASE_URL}/admin/blogs")
    print(f"Categories: {BASE_URL}/admin/categories")
    print(f"Contacts: {BASE_URL}/admin/contacts")
    print(f"GitHub Test: {BASE_URL}/github-test.html")

def show_environment_check():
    """Check environment variables"""
    print("\n🔧 Environment Variables Check:")
    print("=" * 50)
    
    required_vars = [
        "ADMIN_USERNAME",
        "ADMIN_PASSWORD", 
        "GITHUB_USERNAME",
        "SECRET_KEY"
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if var in ["ADMIN_PASSWORD", "SECRET_KEY"]:
                print(f"✅ {var}: {'*' * len(value)}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")

if __name__ == "__main__":
    print("🚀 Admin Panel Test Script")
    print("=" * 50)
    
    # Check environment variables
    show_environment_check()
    
    # Test admin functionality
    if test_admin_login():
        show_admin_urls()
        print("\n🎉 Admin panel is ready to use!")
        print("\n📝 Next steps:")
        print("1. Visit the login URL above")
        print("2. Use credentials: admin / admin1234")
        print("3. Start managing your portfolio content!")
    else:
        print("\n❌ Admin panel setup failed. Please check the errors above.")
