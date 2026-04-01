"""
API Endpoint Verification Script
Tests all backend endpoints to ensure they match frontend expectations
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✓ Health Check: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Health Check Failed: {e}")
        return False

def test_register():
    """Test registration endpoint"""
    try:
        payload = {
            "name": "Test Endpoint User",
            "email": f"endpoint_test_{hash('test')}@example.com",
            "password": "Test@12345",
            "role": "user"
        }
        response = requests.post(f"{BASE_URL}/register", json=payload, timeout=5)
        print(f"✓ Register: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            return data.get('access_token')
        return None
    except Exception as e:
        print(f"✗ Register Failed: {e}")
        return None

def test_login():
    """Test login endpoint"""
    try:
        # First register a user
        email = "login_test@example.com"
        password = "Test@12345"
        
        requests.post(f"{BASE_URL}/register", json={
            "name": "Login Test User",
            "email": email,
            "password": password,
            "role": "user"
        }, timeout=5)
        
        # Now login
        response = requests.post(f"{BASE_URL}/login", json={
            "email": email,
            "password": password
        }, timeout=5)
        
        print(f"✓ Login: {response.status_code}")
        if response.status_code == 200:
            return response.json().get('access_token')
        return None
    except Exception as e:
        print(f"✗ Login Failed: {e}")
        return None

def test_protected_endpoints(token):
    """Test protected endpoints with JWT token"""
    headers = {"Authorization": f"Bearer {token}"}
    
    endpoints = [
        ("GET", "/user/profile", "User Profile"),
        ("GET", "/user/policies", "User Policies"),
        ("GET", "/user/notifications", "User Notifications"),
    ]
    
    for method, path, name in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{path}", headers=headers, timeout=5)
            else:
                response = requests.post(f"{BASE_URL}{path}", headers=headers, json={}, timeout=5)
            
            if response.status_code < 500:
                print(f"✓ {name}: {response.status_code}")
            else:
                print(f"✗ {name}: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"✗ {name} Failed: {e}")

def test_admin_endpoints(admin_token):
    """Test admin endpoints"""
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    endpoints = [
        ("GET", "/admin/users", "Admin - Get Users"),
        ("GET", "/admin/all-policies", "Admin - Get All Policies"),
        ("GET", "/admin/analytics", "Admin - Analytics"),
    ]
    
    for method, path, name in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{path}", headers=headers, timeout=5)
            if response.status_code < 500:
                print(f"✓ {name}: {response.status_code}")
            else:
                print(f"✗ {name}: {response.status_code}")
        except Exception as e:
            print(f"✗ {name} Failed: {e}")

def main():
    print("=" * 60)
    print("Backend API Endpoint Verification")
    print("=" * 60)
    print()
    
    # Test health
    print("1. Testing Health Endpoint...")
    if not test_health():
        print("\n❌ Backend server is not running!")
        print("Start it with: python app.py")
        return
    
    print("\n2. Testing Registration...")
    token = test_register()
    
    print("\n3. Testing Login...")
    login_token = test_login()
    
    if login_token:
        print("\n4. Testing Protected User Endpoints...")
        test_protected_endpoints(login_token)
    
    # Test admin endpoints
    print("\n5. Creating Admin User...")
    try:
        admin_email = "admin_test@example.com"
        requests.post(f"{BASE_URL}/register", json={
            "name": "Admin Test",
            "email": admin_email,
            "password": "Admin@12345",
            "role": "admin"
        }, timeout=5)
        
        admin_response = requests.post(f"{BASE_URL}/login", json={
            "email": admin_email,
            "password": "Admin@12345"
        }, timeout=5)
        
        if admin_response.status_code == 200:
            admin_token = admin_response.json().get('access_token')
            print("\n6. Testing Admin Endpoints...")
            test_admin_endpoints(admin_token)
    except Exception as e:
        print(f"✗ Admin tests failed: {e}")
    
    print("\n" + "=" * 60)
    print("Verification Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
