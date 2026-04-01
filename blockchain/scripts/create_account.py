"""
Create a new Algorand testnet account and display credentials.
"""
from algosdk import account, mnemonic

def create_algorand_account():
    """Generate a new Algorand account."""
    private_key, address = account.generate_account()
    mnemonic_phrase = mnemonic.from_private_key(private_key)
    
    print("=" * 70)
    print("NEW ALGORAND TESTNET ACCOUNT CREATED")
    print("=" * 70)
    print()
    print("Account Address:")
    print(address)
    print()
    print("Mnemonic (25 words) - SAVE THIS SECURELY:")
    print(mnemonic_phrase)
    print()
    print("=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print()
    print("1. Copy the Address above")
    print("2. Go to: https://bank.testnet.algorand.network/")
    print("3. Paste your address and click 'Dispense'")
    print("4. Wait 10 seconds for testnet ALGOs to arrive")
    print()
    print("5. Add to backend/.env:")
    print(f"   ALGORAND_CREATOR_MNEMONIC=\"{mnemonic_phrase}\"")
    print()
    print("6. Run: python blockchain/scripts/deploy_contract.py")
    print()
    print("=" * 70)
    print("⚠️  IMPORTANT: Save the mnemonic phrase - it cannot be recovered!")
    print("=" * 70)
    
    return address, mnemonic_phrase

if __name__ == "__main__":
    create_algorand_account()
