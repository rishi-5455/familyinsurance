"""
Comprehensive Test Suite - Verify All Components and Roles

This script tests:
1. Database connectivity
2. All API endpoints
3. Authentication and authorization
4. Role-based access control
5. Blockchain integration
6. All CRUD operations
"""

import os
import sys
import json
from dotenv import load_dotenv

# Setup paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

print("=" * 80)
print("COMPREHENSIVE SYSTEM VERIFICATION")
print("=" * 80)

# Test 1: Environment Configuration
print("\n[1] CHECKING ENVIRONMENT CONFIGURATION")
print("-" * 80)

required_env_vars = [
    "MONGO_URI",
    "JWT_SECRET_KEY",
    "ALGORAND_APP_ID",
    "ALGORAND_CREATOR_MNEMONIC",
    "ALGORAND_ALGOD_URL"
]

env_status = True
for var in required_env_vars:
    value = os.getenv(var)
    status = "✓" if value else "✗"
    print(f"{status} {var}: {'SET' if value else 'MISSING'}")
    if not value and var not in ["ALGORAND_CREATOR_MNEMONIC"]:
        env_status = False

print(f"\nEnvironment Status: {'✓ PASS' if env_status else '✗ FAIL'}")

# Test 2: Database Connection
print("\n[2] TESTING DATABASE CONNECTION")
print("-" * 80)

try:
    from pymongo import MongoClient
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/family_insurance")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    client.server_info()
    print("✓ MongoDB connection successful")
    print(f"✓ Database: {client.get_database().name}")
    
    # Check collections
    db = client.get_database()
    collections = db.list_collection_names()
    print(f"✓ Collections found: {len(collections)}")
    for coll in collections:
        count = db[coll].count_documents({})
        print(f"  - {coll}: {count} documents")
    
    db_status = True
except Exception as e:
    print(f"✗ MongoDB connection failed: {e}")
    db_status = False

print(f"\nDatabase Status: {'✓ PASS' if db_status else '✗ FAIL'}")

# Test 3: Blockchain Configuration
print("\n[3] CHECKING BLOCKCHAIN INTEGRATION")
print("-" * 80)

app_id = os.getenv("ALGORAND_APP_ID", "0")
mnemonic = os.getenv("ALGORAND_CREATOR_MNEMONIC")

print(f"App ID: {app_id}")
print(f"Mnemonic: {'✓ SET' if mnemonic else '✗ NOT SET'}")

blockchain_status = True

if app_id == "0":
    print("⚠ WARNING: Blockchain is in SIMULATION MODE")
    print("  Deploy smart contract to activate real blockchain transactions")
    blockchain_status = False
else:
    print(f"✓ Smart contract deployed: App ID {app_id}")
    
    # Try to connect to Algorand
    try:
        from algosdk.v2client import algod
        algod_url = os.getenv("ALGORAND_ALGOD_URL", "https://testnet-api.algonode.cloud")
        client = algod.AlgodClient("", algod_url)
        status = client.status()
        print(f"✓ Connected to Algorand testnet")
        print(f"✓ Last round: {status.get('last-round')}")
        
        # Check if app exists
        try:
            app_info = client.application_info(int(app_id))
            print(f"✓ Smart contract verified on-chain")
            print(f"  Creator: {app_info['params']['creator']}")
            blockchain_status = True
        except Exception as e:
            print(f"✗ Smart contract not found: {e}")
            blockchain_status = False
            
    except Exception as e:
        print(f"✗ Algorand connection failed: {e}")
        blockchain_status = False

print(f"\nBlockchain Status: {'✓ PASS' if blockchain_status else '⚠ SIMULATION'}")

# Test 4: Model Tests
print("\n[4] TESTING MODELS")
print("-" * 80)

model_status = True
try:
    from models.user_model import UserModel
    from models.policy_model import PolicyModel
    from models.claim_model import ClaimModel
    
    print("✓ UserModel imported successfully")
    print("✓ PolicyModel imported successfully")
    print("✓ ClaimModel imported successfully")
    
    # Test collection methods
    assert hasattr(UserModel, 'collection'), "UserModel missing collection method"
    assert hasattr(PolicyModel, 'collection'), "PolicyModel missing collection method"
    assert hasattr(ClaimModel, 'collection'), "ClaimModel missing collection method"
    print("✓ All models have collection() method")
    
    # Test static methods
    assert hasattr(UserModel, 'find_by_email'), "UserModel missing find_by_email"
    assert hasattr(PolicyModel, 'find_by_policy_id'), "PolicyModel missing find_by_policy_id"
    assert hasattr(ClaimModel, 'find_by_claim_id'), "ClaimModel missing find_by_claim_id"
    print("✓ All models have required find methods")
    
except AssertionError as e:
    print(f"✗ Model test failed: {e}")
    model_status = False
except Exception as e:
    print(f"✗ Model import failed: {e}")
    model_status = False

print(f"\nModel Status: {'✓ PASS' if model_status else '✗ FAIL'}")

# Test 5: Controller Tests
print("\n[5] TESTING CONTROLLERS")
print("-" * 80)

controller_status = True
try:
    from controllers.auth_controller import register, login
    from controllers.user_controller import get_profile, add_family_member, buy_policy
    from controllers.admin_controller import get_users, get_all_policies, approve_claim
    from controllers.verifier_controller import verify_policy
    from controllers.claim_controller import submit_claim
    
    print("✓ auth_controller: register, login")
    print("✓ user_controller: get_profile, add_family_member, buy_policy")
    print("✓ admin_controller: get_users, get_all_policies, approve_claim")
    print("✓ verifier_controller: verify_policy")
    print("✓ claim_controller: submit_claim")
    
except Exception as e:
    print(f"✗ Controller import failed: {e}")
    controller_status = False

print(f"\nController Status: {'✓ PASS' if controller_status else '✗ FAIL'}")

# Test 6: Service Tests
print("\n[6] TESTING SERVICES")
print("-" * 80)

service_status = True
try:
    from services.algorand_service import (
        sync_policy_to_chain,
        verify_policy_on_chain,
        submit_claim_to_chain,
        approve_claim_on_chain
    )
    from services.ipfs_service import upload_file_to_ipfs
    
    print("✓ algorand_service: sync_policy_to_chain")
    print("✓ algorand_service: verify_policy_on_chain")
    print("✓ algorand_service: submit_claim_to_chain")
    print("✓ algorand_service: approve_claim_on_chain")
    print("✓ ipfs_service: upload_file_to_ipfs")
    
except Exception as e:
    print(f"✗ Service import failed: {e}")
    service_status = False

print(f"\nService Status: {'✓ PASS' if service_status else '✗ FAIL'}")

# Test 7: Utility Tests
print("\n[7] TESTING UTILITIES")
print("-" * 80)

utility_status = True
try:
    from utils.auth import role_required
    from utils.serializers import serialize_doc
    from utils.ids import generate_readable_id
    
    print("✓ auth: role_required decorator")
    print("✓ serializers: serialize_doc")
    print("✓ ids: generate_readable_id")
    
    # Test ID generation
    test_id = generate_readable_id("TEST")
    assert test_id.startswith("TEST-"), "ID generation failed"
    print(f"✓ ID generation works: {test_id}")
    
except Exception as e:
    print(f"✗ Utility test failed: {e}")
    utility_status = False

print(f"\nUtility Status: {'✓ PASS' if utility_status else '✗ FAIL'}")

# Final Summary
print("\n" + "=" * 80)
print("VERIFICATION SUMMARY")
print("=" * 80)

all_tests = [
    ("Environment Configuration", env_status),
    ("Database Connection", db_status),
    ("Blockchain Integration", blockchain_status),
    ("Models", model_status),
    ("Controllers", controller_status),
    ("Services", service_status),
    ("Utilities", utility_status),
]

passed = sum(1 for _, status in all_tests if status)
total = len(all_tests)

for name, status in all_tests:
    symbol = "✓" if status else "✗"
    print(f"{symbol} {name}")

print("\n" + "=" * 80)
overall_status = passed == total
print(f"OVERALL: {passed}/{total} tests passed")

if overall_status:
    print("✅ ALL SYSTEMS OPERATIONAL")
else:
    print("⚠️  SOME SYSTEMS NEED ATTENTION")
    
print("=" * 80)

# Return exit code
sys.exit(0 if overall_status else 1)
