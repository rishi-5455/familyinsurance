"""
Check if Algorand account is funded and ready for deployment.
"""
import os
from algosdk.v2client import algod
from algosdk import mnemonic

def check_account_balance():
    """Check if the account has been funded."""
    algod_url = "https://testnet-api.algonode.cloud"
    algod_token = ""
    client = algod.AlgodClient(algod_token, algod_url)
    
    # Get mnemonic from environment
    mnemonic_phrase = os.getenv("ALGORAND_CREATOR_MNEMONIC")
    if not mnemonic_phrase:
        # Try to read from .env file in parent directory
        env_path = os.path.join(os.path.dirname(__file__), "..", "..", "backend", ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.startswith("ALGORAND_CREATOR_MNEMONIC="):
                        mnemonic_phrase = line.split("=", 1)[1].strip().strip('"')
                        break
    
    if not mnemonic_phrase:
        print("❌ ALGORAND_CREATOR_MNEMONIC not found in backend/.env")
        return False
    
    # Get address from mnemonic
    private_key = mnemonic.to_private_key(mnemonic_phrase)
    from algosdk import account
    address = account.address_from_private_key(private_key)
    
    print("=" * 70)
    print("CHECKING ACCOUNT STATUS")
    print("=" * 70)
    print(f"Address: {address}")
    print()
    
    try:
        account_info = client.account_info(address)
        balance = account_info.get('amount', 0) / 1_000_000  # Convert microAlgos to Algos
        
        print(f"✓ Account Balance: {balance} ALGO")
        print()
        
        if balance >= 1.0:
            print("✓ Account is funded and ready!")
            print()
            print("=" * 70)
            print("NEXT STEPS:")
            print("=" * 70)
            print("1. Compile contract:")
            print("   python blockchain/scripts/compile_contract.py")
            print()
            print("2. Deploy contract:")
            print("   python blockchain/scripts/deploy_contract.py")
            print()
            return True
        else:
            print("⚠️  Account needs funding!")
            print(f"   Current: {balance} ALGO")
            print(f"   Needed: At least 1 ALGO")
            print()
            print("Fund your account:")
            print(f"1. Go to: https://bank.testnet.algorand.network/")
            print(f"2. Paste address: {address}")
            print(f"3. Click 'Dispense' to get 10 testnet ALGOs")
            print()
            return False
            
    except Exception as e:
        print(f"❌ Error checking account: {e}")
        print()
        print("The account might not be activated yet.")
        print("Fund it first at: https://bank.testnet.algorand.network/")
        return False

if __name__ == "__main__":
    check_account_balance()
