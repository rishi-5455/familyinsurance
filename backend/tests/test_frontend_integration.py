"""
FRONTEND-BACKEND VALIDATION SCRIPT
Run this to automatically detect common issues
"""

import requests
import json
from colorama import init, Fore, Style

init()

BASE_URL = "http://localhost:5000/api"

def test(name, fn):
    try:
        print(f"\n{Fore.CYAN}Testing: {name}{Style.RESET_ALL}")
        fn()
        print(f"{Fore.GREEN}✓ PASSED{Style.RESET_ALL}")
        return True
    except AssertionError as e:
        print(f"{Fore.RED}✗ FAILED: {e}{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}✗ ERROR: {e}{Style.RESET_ALL}")
        return False

def test_backend_running():
    r = requests.get(f"{BASE_URL}/../")
    assert r.status_code in [200, 404], "Backend not responding"

def test_register():
    payload = {
        "name": "Test User",
        "email": f"testuser_{import_random()}@test.com",
        "password": "Test@123",
        "role": "user"
    }
    r = requests.post(f"{BASE_URL}/register", json=payload)
    assert r.status_code == 201, f"Register failed: {r.text}"

def test_login():
    # First register
    email = f"login_test_{import_random()}@test.com"
    requests.post(f"{BASE_URL}/register", json={
        "name": "Login Test",
        "email": email,
        "password": "Test@123",
        "role": "user"
    })
    
    # Then login
    r = requests.post(f"{BASE_URL}/login", json={
        "email": email,
        "password": "Test@123"
    })
    assert r.status_code == 200, f"Login failed: {r.text}"
    data = r.json()
    assert "access_token" in data, "No access_token in response"
    assert "user" in data, "No user in response"
    return data["access_token"]

def test_protected_endpoint():
    token = test_login()
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/user/profile", headers=headers)
    assert r.status_code == 200, f"Protected endpoint failed: {r.text}"

def test_id_field_in_response():
    """Check if _id is properly converted to id"""
    token = test_login()
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/user/profile", headers=headers)
    data = r.json()
    assert "id" in data, "Response has _id instead of id - serialization issue!"

def import_random():
    import random
    return random.randint(1000, 9999)

def main():
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}FRONTEND-BACKEND VALIDATION{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    
    print(f"\n{Fore.MAGENTA}Checking Backend Connection...{Style.RESET_ALL}")
    print(f"Base URL: {BASE_URL}")
    
    tests = [
        ("Backend is running", test_backend_running),
        ("User registration works", test_register),
        ("User login works", test_login),
        ("Protected endpoints work", test_protected_endpoint),
        ("ID field serialization (_id -> id)", test_id_field_in_response),
    ]
    
    passed = 0
    failed = 0
    
    for name, fn in tests:
        if test(name, fn):
            passed += 1
        else:
            failed += 1
    
    print(f"\n{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Passed: {passed}{Style.RESET_ALL}")
    print(f"{Fore.RED}Failed: {failed}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    
    if failed > 0:
        print(f"\n{Fore.RED}⚠️  ISSUES DETECTED!{Style.RESET_ALL}")
        print("Check the failed tests above and fix them.")
        print("\nCommon fixes:")
        print("1. Make sure backend is running: cd backend; python app.py")
        print("2. Check MongoDB is running: mongo")
        print("3. Check .env file has correct values")
        print("4. Restart backend after making changes")
    else:
        print(f"\n{Fore.GREEN}✓ ALL TESTS PASSED!{Style.RESET_ALL}")
        print("Backend API is working correctly.")
        print("\nIf frontend still has issues:")
        print("1. Check browser console (F12) for errors")
        print("2. Verify API URL in frontend/.env.local")
        print("3. Clear browser localStorage and try again")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Aborted{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        print("\nMake sure:")
        print("1. Backend is running on http://localhost:5000")
        print("2. MongoDB is running")
        print("3. Install colorama: pip install colorama")
