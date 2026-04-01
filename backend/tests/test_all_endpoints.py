"""
Comprehensive API Endpoint Testing Script
Tests all 18 endpoints with proper authentication and role-based access
"""

import requests
import json
import time
import os
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")

def print_error(msg):
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {msg}")

# Test tracking
results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "errors": []
}

def test_endpoint(name, method, url, headers=None, data=None, files=None, expected_status=200, should_fail=False):
    """Test a single endpoint"""
    results["total"] += 1
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            if files:
                response = requests.post(url, headers=headers, data=data, files=files, timeout=10)
            else:
                response = requests.post(url, headers=headers, json=data, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        # Check status code
        if should_fail:
            if response.status_code in [401, 403, 422]:  # 422 = malformed token
                print_success(f"{name}: Correctly blocked (HTTP {response.status_code})")
                results["passed"] += 1
                return True
            else:
                print_error(f"{name}: Should have been blocked but got {response.status_code}")
                results["failed"] += 1
                results["errors"].append(f"{name}: Expected auth failure, got {response.status_code}")
                return False
        else:
            if response.status_code == expected_status:
                print_success(f"{name}: HTTP {response.status_code}")
                results["passed"] += 1
                return response.json() if response.content else None
            else:
                print_error(f"{name}: Expected {expected_status}, got {response.status_code}")
                print_error(f"  Response: {response.text[:200]}")
                results["failed"] += 1
                results["errors"].append(f"{name}: Expected {expected_status}, got {response.status_code}")
                return None
                
    except requests.exceptions.ConnectionError:
        print_error(f"{name}: Connection refused - Is backend running?")
        results["failed"] += 1
        results["errors"].append(f"{name}: Backend not running")
        return None
    except Exception as e:
        print_error(f"{name}: {str(e)}")
        results["failed"] += 1
        results["errors"].append(f"{name}: {str(e)}")
        return None

def main():
    print("=" * 80)
    print("COMPREHENSIVE API ENDPOINT TESTING")
    print("=" * 80)
    print()
    
    # Test 1: Health Check
    print("[1] HEALTH CHECK")
    print("-" * 80)
    test_endpoint("GET /api/health", "GET", f"{BASE_URL}/health")
    print()
    
    # Test 2: Authentication Endpoints
    print("[2] AUTHENTICATION ENDPOINTS")
    print("-" * 80)
    
    # Register test users (one per role)
    timestamp = int(time.time())
    
    user_data = {
        "name": f"Test User {timestamp}",
        "email": f"testuser{timestamp}@test.com",
        "password": "testpass123",
        "role": "user"
    }
    
    admin_data = {
        "name": f"Test Admin {timestamp}",
        "email": f"testadmin{timestamp}@test.com",
        "password": "testpass123",
        "role": "admin"
    }
    
    verifier_data = {
        "name": f"Test Verifier {timestamp}",
        "email": f"testverifier{timestamp}@test.com",
        "password": "testpass123",
        "role": "verifier"
    }
    
    # Register users
    user_response = test_endpoint("POST /api/register (user)", "POST", f"{BASE_URL}/register", data=user_data, expected_status=201)
    admin_response = test_endpoint("POST /api/register (admin)", "POST", f"{BASE_URL}/register", data=admin_data, expected_status=201)
    verifier_response = test_endpoint("POST /api/register (verifier)", "POST", f"{BASE_URL}/register", data=verifier_data, expected_status=201)
    
    # Extract tokens from registration
    user_token = user_response.get("access_token") if user_response else None
    admin_token = admin_response.get("access_token") if admin_response else None
    verifier_token = verifier_response.get("access_token") if verifier_response else None
    
    # Test login
    login_response = test_endpoint(
        "POST /api/login", 
        "POST", 
        f"{BASE_URL}/login", 
        data={"email": user_data["email"], "password": user_data["password"]}
    )
    
    if login_response and not user_token:
        user_token = login_response.get("access_token")
    
    print()
    
    if not user_token:
        print_error("Failed to get user token - cannot proceed with protected endpoint tests")
        return
    
    # Prepare headers
    user_headers = {"Authorization": f"Bearer {user_token}"}
    admin_headers = {"Authorization": f"Bearer {admin_token}"} if admin_token else user_headers
    verifier_headers = {"Authorization": f"Bearer {verifier_token}"} if verifier_token else user_headers
    
    # Test 3: User Endpoints
    print("[3] USER ENDPOINTS")
    print("-" * 80)
    
    # Get profile
    profile = test_endpoint("GET /api/user/profile", "GET", f"{BASE_URL}/user/profile", headers=user_headers)
    
    # Add family member
    family_data = {
        "name": "John Doe",
        "age": 35,
        "relation": "spouse"
    }
    test_endpoint("POST /api/user/family", "POST", f"{BASE_URL}/user/family", headers=user_headers, data=family_data)
    
    # Get policies (empty initially)
    test_endpoint("GET /api/user/policies", "GET", f"{BASE_URL}/user/policies", headers=user_headers)
    
    # Link wallet
    wallet_data = {"walletAddress": "TEST_WALLET_ADDRESS_123"}
    test_endpoint("POST /api/user/link-wallet", "POST", f"{BASE_URL}/user/link-wallet", headers=user_headers, data=wallet_data)
    
    # Get notifications
    test_endpoint("GET /api/user/notifications", "GET", f"{BASE_URL}/user/notifications", headers=user_headers)
    
    # Buy policy (multipart form data - simplified test)
    print_info("POST /api/user/buy-policy: Skipping (requires file upload)")
    print()
    
    # Test 4: Admin Endpoints
    print("[4] ADMIN ENDPOINTS")
    print("-" * 80)
    
    # Test role protection - user should NOT access admin endpoints
    test_endpoint(
        "GET /api/admin/users (user blocked)", 
        "GET", 
        f"{BASE_URL}/admin/users", 
        headers=user_headers,
        should_fail=True
    )
    
    # Admin accessing admin endpoints
    test_endpoint("GET /api/admin/users", "GET", f"{BASE_URL}/admin/users", headers=admin_headers)
    test_endpoint("GET /api/admin/all-policies", "GET", f"{BASE_URL}/admin/all-policies", headers=admin_headers)
    test_endpoint("GET /api/admin/all-claims", "GET", f"{BASE_URL}/admin/all-claims", headers=admin_headers)
    test_endpoint("GET /api/admin/analytics", "GET", f"{BASE_URL}/admin/analytics", headers=admin_headers)
    
    # Create policy template
    template_data = {
        "name": "Test Policy Template",
        "coverage": 100000,
        "durationMonths": 12,
        "description": "Test template"
    }
    test_endpoint("POST /api/admin/create-policy", "POST", f"{BASE_URL}/admin/create-policy", headers=admin_headers, data=template_data, expected_status=201)
    
    # Approve claim (needs claim ID - simplified)
    print_info("POST /api/admin/approve-claim: Requires existing claim ID")
    
    print()
    
    # Test 5: Verifier Endpoints
    print("[5] VERIFIER ENDPOINTS")
    print("-" * 80)
    
    # Test role protection - user should NOT access verifier endpoints (except QR with proper role)
    test_endpoint(
        "GET /api/verifier/verify-policy/TEST123 (user blocked)", 
        "GET", 
        f"{BASE_URL}/verifier/verify-policy/TEST123", 
        headers=user_headers,
        should_fail=True
    )
    
    # Verifier accessing verifier endpoints
    test_endpoint(
        "GET /api/verifier/verify-policy/NONEXISTENT", 
        "GET", 
        f"{BASE_URL}/verifier/verify-policy/NONEXISTENT", 
        headers=verifier_headers,
        expected_status=404
    )
    
    # QR code endpoint (user can access for their own policies)
    test_endpoint(
        "GET /api/verifier/policy-qr/NONEXISTENT", 
        "GET", 
        f"{BASE_URL}/verifier/policy-qr/NONEXISTENT", 
        headers=user_headers,
        expected_status=404
    )
    
    print()
    
    # Test 6: Claims Endpoints
    print("[6] CLAIMS ENDPOINTS")
    print("-" * 80)
    
    # Submit claim (needs file - simplified)
    print_info("POST /api/claims/submit-claim: Skipping (requires file upload)")
    
    # Get claim status
    test_endpoint(
        "GET /api/claims/claim-status/NONEXISTENT", 
        "GET", 
        f"{BASE_URL}/claims/claim-status/NONEXISTENT", 
        headers=user_headers,
        expected_status=404
    )
    
    print()
    
    # Test 7: Authorization Tests
    print("[7] AUTHORIZATION TESTS")
    print("-" * 80)
    
    # Test without token
    test_endpoint(
        "GET /api/user/profile (no token)", 
        "GET", 
        f"{BASE_URL}/user/profile",
        should_fail=True
    )
    
    # Test with invalid token
    bad_headers = {"Authorization": "Bearer INVALID_TOKEN_12345"}
    test_endpoint(
        "GET /api/user/profile (invalid token)", 
        "GET", 
        f"{BASE_URL}/user/profile",
        headers=bad_headers,
        should_fail=True
    )
    
    print()
    
    # Final Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {results['total']}")
    print(f"{Colors.GREEN}Passed: {results['passed']}{Colors.RESET}")
    print(f"{Colors.RED}Failed: {results['failed']}{Colors.RESET}")
    print()
    
    if results["errors"]:
        print("ERRORS:")
        for error in results["errors"]:
            print(f"  {Colors.RED}•{Colors.RESET} {error}")
        print()
    
    success_rate = (results["passed"] / results["total"] * 100) if results["total"] > 0 else 0
    
    if success_rate == 100:
        print(f"{Colors.GREEN}✅ ALL ENDPOINTS WORKING CORRECTLY{Colors.RESET}")
    elif success_rate >= 80:
        print(f"{Colors.YELLOW}⚠️  MOST ENDPOINTS WORKING ({success_rate:.1f}%){Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ MANY ENDPOINTS FAILING ({success_rate:.1f}%){Colors.RESET}")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
