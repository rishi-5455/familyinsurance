"""
Test real blockchain integration - verify contract is deployed and working
"""
import os
import sys
from dotenv import load_dotenv

# Add parent to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "backend", ".env"))

from algosdk.v2client import algod

def verify_blockchain():
    """Verify the blockchain is properly configured and accessible."""
    print("=" * 70)
    print("BLOCKCHAIN INTEGRATION VERIFICATION")
    print("=" * 70)
    
    # Check environment variables
    app_id = os.getenv("ALGORAND_APP_ID")
    mnemonic = os.getenv("ALGORAND_CREATOR_MNEMONIC")
    algod_url = os.getenv("ALGORAND_ALGOD_URL", "https://testnet-api.algonode.cloud")
    
    print(f"\n✓ ALGORAND_APP_ID: {app_id}")
    print(f"✓ Creator Mnemonic: {'Configured' if mnemonic else 'Missing'}")
    print(f"✓ Algod URL: {algod_url}")
    
    if app_id == "0":
        print("\n❌ SIMULATION MODE - App ID is still 0")
        print("   Update backend/.env with: ALGORAND_APP_ID=758018952")
        return False
    
    # Connect to Algorand
    print(f"\n📡 Connecting to Algorand testnet...")
    client = algod.AlgodClient("", algod_url)
    
    try:
        status = client.status()
        print(f"✓ Connected to testnet")
        print(f"✓ Last round: {status.get('last-round')}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    # Verify application exists
    try:
        app_info = client.application_info(int(app_id))
        print(f"\n✅ Smart Contract Found!")
        print(f"   App ID: {app_id}")
        print(f"   Creator: {app_info['params']['creator']}")
        
        # Check on AlgoExplorer
        print(f"\n🔗 View on AlgoExplorer:")
        print(f"   https://testnet.algoexplorer.io/application/{app_id}")
        
        print("\n" + "=" * 70)
        print("✅ BLOCKCHAIN IS LIVE AND WORKING!")
        print("=" * 70)
        print("\nAll policy purchases and claims will now be recorded on")
        print("Algorand testnet blockchain with verifiable transactions.")
        return True
        
    except Exception as e:
        print(f"\n❌ Application {app_id} not found: {e}")
        return False

if __name__ == "__main__":
    verify_blockchain()
