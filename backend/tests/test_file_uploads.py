"""
Test file upload endpoints (buy-policy, submit-claim, approve-claim)
"""

import requests
import io
import json

BASE_URL = "http://localhost:5000/api"

def test_buy_policy():
    """Test buy policy with file upload"""
    print("\n=== Testing POST /api/user/buy-policy ===")
    
    # 1. Register and login user
    register_data = {
        "name": "Policy Buyer",
        "email": f"buyer_{int(__import__('time').time())}@test.com",
        "password": "Test@123",
        "role": "user"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    if response.status_code != 201:
        print(f"❌ Registration failed: {response.status_code}")
        return False
    
    token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Buy policy with file upload
    policy_data = {
        "coverage": "50000",
        "durationMonths": "12",
        "walletAddress": "ALGO123TEST456",
        "familyMembers": json.dumps([
            {"name": "Jane Doe", "age": 28, "relation": "spouse"},
            {"name": "John Doe Jr", "age": 5, "relation": "child"}
        ])
    }
    
    # Create a fake PDF file
    fake_pdf = io.BytesIO(b"%PDF-1.4 fake policy document content")
    fake_pdf.name = "policy_document.pdf"
    
    files = {"document": ("policy.pdf", fake_pdf, "application/pdf")}
    
    response = requests.post(
        f"{BASE_URL}/user/buy-policy",
        headers=headers,
        data=policy_data,
        files=files
    )
    
    if response.status_code == 201:
        print(f"✅ Policy created successfully")
        result = response.json()
        print(f"   Policy ID: {result['policy']['policyId']}")
        print(f"   Coverage: ${result['policy']['coverage']}")
        print(f"   Status: {result['policy']['status']}")
        return result['policy']['policyId']
    else:
        print(f"❌ Policy creation failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None


def test_submit_claim(policy_id=None):
    """Test submit claim with file upload"""
    print("\n=== Testing POST /api/claims/submit-claim ===")
    
    if not policy_id:
        # Create a policy first
        policy_id = test_buy_policy()
        if not policy_id:
            print("❌ Cannot test claim submission without a policy")
            return None
    
    # Get the token from the current session or create new user
    register_data = {
        "name": "Claim Submitter",
        "email": f"claimer_{int(__import__('time').time())}@test.com",
        "password": "Test@123",
        "role": "user"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a policy for this user first
    policy_data = {
        "coverage": "25000",
        "durationMonths": "6",
        "walletAddress": "ALGO_WALLET_TEST",
        "familyMembers": "[]"
    }
    
    fake_pdf = io.BytesIO(b"%PDF-1.4 fake policy doc")
    files = {"document": ("policy.pdf", fake_pdf, "application/pdf")}
    
    policy_response = requests.post(
        f"{BASE_URL}/user/buy-policy",
        headers=headers,
        data=policy_data,
        files=files
    )
    
    if policy_response.status_code != 201:
        print(f"❌ Failed to create policy for claim test")
        return None
    
    user_policy_id = policy_response.json()['policy']['policyId']
    
    # Submit claim
    claim_data = {
        "policyId": user_policy_id,
        "reason": "Medical emergency - hospital bills"
    }
    
    # Create fake medical document
    fake_doc = io.BytesIO(b"Medical invoice: $5000 treatment cost")
    files = {"document": ("medical_bill.pdf", fake_doc, "application/pdf")}
    
    response = requests.post(
        f"{BASE_URL}/claims/submit-claim",
        headers=headers,
        data=claim_data,
        files=files
    )
    
    if response.status_code == 201:
        print(f"✅ Claim submitted successfully")
        result = response.json()
        print(f"   Claim ID: {result['claim']['claimId']}")
        print(f"   Policy ID: {result['claim']['policyId']}")
        print(f"   Status: {result['claim']['status']}")
        return result['claim']['claimId']
    else:
        print(f"❌ Claim submission failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None


def test_approve_claim(claim_id=None):
    """Test approve claim endpoint"""
    print("\n=== Testing POST /api/admin/approve-claim ===")
    
    if not claim_id:
        claim_id = test_submit_claim()
        if not claim_id:
            print("❌ Cannot test claim approval without a claim")
            return False
    
    # Register admin
    admin_data = {
        "name": "Claim Approver",
        "email": f"approver_{int(__import__('time').time())}@test.com",
        "password": "Admin@123",
        "role": "admin"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=admin_data)
    admin_token = response.json().get("access_token")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Approve claim
    approval_data = {
        "claimId": claim_id,
        "action": "approve"
    }
    
    response = requests.post(
        f"{BASE_URL}/admin/approve-claim",
        headers=admin_headers,
        json=approval_data
    )
    
    if response.status_code == 200:
        print(f"✅ Claim approved successfully")
        result = response.json()
        print(f"   Message: {result['message']}")
        print(f"   Claim ID: {result['claimId']}")
        return True
    else:
        print(f"❌ Claim approval failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return False


def test_invalid_inputs():
    """Test validation for invalid inputs"""
    print("\n=== Testing Input Validation ===")
    
    # Register user
    register_data = {
        "name": "Validator",
        "email": f"validator_{int(__import__('time').time())}@test.com",
        "password": "Test@123",
        "role": "user"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Invalid coverage (not a number)
    print("\n1. Testing invalid coverage value...")
    policy_data = {
        "coverage": "invalid_number",
        "durationMonths": "12",
        "walletAddress": "TEST",
        "familyMembers": "[]"
    }
    
    response = requests.post(
        f"{BASE_URL}/user/buy-policy",
        headers=headers,
        data=policy_data
    )
    
    if response.status_code == 400:
        print(f"   ✅ Correctly rejected invalid coverage: {response.json()['message']}")
    else:
        print(f"   ❌ Should have rejected invalid coverage, got {response.status_code}")
    
    # Test 2: Zero coverage
    print("\n2. Testing zero coverage value...")
    policy_data["coverage"] = "0"
    
    response = requests.post(
        f"{BASE_URL}/user/buy-policy",
        headers=headers,
        data=policy_data
    )
    
    if response.status_code == 400:
        print(f"   ✅ Correctly rejected zero coverage: {response.json()['message']}")
    else:
        print(f"   ❌ Should have rejected zero coverage, got {response.status_code}")
    
    # Test 3: Invalid duration
    print("\n3. Testing invalid duration...")
    policy_data = {
        "coverage": "50000",
        "durationMonths": "not_a_number",
        "walletAddress": "TEST",
        "familyMembers": "[]"
    }
    
    response = requests.post(
        f"{BASE_URL}/user/buy-policy",
        headers=headers,
        data=policy_data
    )
    
    if response.status_code == 400:
        print(f"   ✅ Correctly rejected invalid duration: {response.json()['message']}")
    else:
        print(f"   ❌ Should have rejected invalid duration, got {response.status_code}")


if __name__ == "__main__":
    print("=" * 80)
    print("FILE UPLOAD & VALIDATION ENDPOINT TESTING")
    print("=" * 80)
    
    try:
        # Test buy policy
        policy_id = test_buy_policy()
        
        # Test submit claim
        claim_id = test_submit_claim()
        
        # Test approve claim
        if claim_id:
            test_approve_claim(claim_id)
        
        # Test invalid inputs
        test_invalid_inputs()
        
        print("\n" + "=" * 80)
        print("✅ FILE UPLOAD TESTS COMPLETED")
        print("=" * 80)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend at http://localhost:5000")
        print("   Make sure the backend is running: cd backend && python app.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
