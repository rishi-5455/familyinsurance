import os
import json
import base64
from dotenv import load_dotenv
from algosdk.v2client import algod
from algosdk import account, transaction, mnemonic
from algosdk.abi import Contract

# Load environment from backend/.env
backend_env = os.path.join(os.path.dirname(__file__), "..", "..", "backend", ".env")
load_dotenv(backend_env)


def main():
    algod_url = os.getenv("ALGORAND_ALGOD_URL", "https://testnet-api.algonode.cloud")
    algod_token = os.getenv("ALGORAND_ALGOD_TOKEN", "")
    
    client = algod.AlgodClient(algod_token, algod_url)
    status = client.status()
    print(f"✓ Connected to Algorand {os.getenv('ALGORAND_NETWORK', 'testnet')}")
    print(f"✓ Last round: {status.get('last-round')}")
    
    # Check for creator account
    creator_mnemonic = os.getenv("ALGORAND_CREATOR_MNEMONIC")
    creator_private_key = os.getenv("ALGORAND_CREATOR_PRIVATE_KEY")
    
    if not creator_private_key and not creator_mnemonic:
        print("\n❌ No creator account configured.")
        print("To deploy the smart contract:")
        print("1. Create an Algorand account on testnet")
        print("2. Fund it with testnet ALGO from https://bank.testnet.algorand.network/")
        print("3. Set ALGORAND_CREATOR_PRIVATE_KEY in backend/.env")
        print("4. Run: python blockchain/scripts/compile_contract.py")
        print("5. Run this script again")
        return
    
    if creator_mnemonic:
        creator_private_key = mnemonic.to_private_key(creator_mnemonic)
    
    creator_address = account.address_from_private_key(creator_private_key)
    print(f"✓ Creator account: {creator_address}")
    
    # Check balance
    try:
        account_info = client.account_info(creator_address)
        balance = account_info.get('amount', 0) / 1_000_000  # Convert microAlgos
        print(f"✓ Balance: {balance} ALGO")
        
        if balance < 0.1:
            print("⚠ Low balance. Fund account at: https://bank.testnet.algorand.network/")
            return
    except Exception as e:
        print(f"❌ Could not fetch account info: {e}")
        return
    
    # Load compiled TEAL
    build_dir = os.path.join(os.path.dirname(__file__), "..", "build")
    approval_path = os.path.join(build_dir, "approval.teal")
    clear_path = os.path.join(build_dir, "clear.teal")
    contract_path = os.path.join(build_dir, "contract.json")
    
    if not os.path.exists(approval_path):
        print("❌ Contract not compiled. Run: python blockchain/scripts/compile_contract.py")
        return
    
    with open(approval_path, "r") as f:
        approval_program = f.read()
    
    with open(clear_path, "r") as f:
        clear_program = f.read()
    
    print("✓ Loaded compiled TEAL programs")
    
    # Compile programs to bytecode
    approval_result = client.compile(approval_program)
    clear_result = client.compile(clear_program)
    
    approval_binary = base64.b64decode(approval_result["result"])
    clear_binary = base64.b64decode(clear_result["result"])
    
    print("✓ Programs compiled to bytecode")
    
    # Create application transaction
    params = client.suggested_params()
    
    # Define schema
    global_schema = transaction.StateSchema(num_uints=1, num_byte_slices=5)
    local_schema = transaction.StateSchema(num_uints=0, num_byte_slices=0)
    
    txn = transaction.ApplicationCreateTxn(
        sender=creator_address,
        sp=params,
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=approval_binary,
        clear_program=clear_binary,
        global_schema=global_schema,
        local_schema=local_schema,
    )
    
    # Sign and send
    signed_txn = txn.sign(creator_private_key)
    
    print("📡 Submitting contract deployment transaction...")
    
    try:
        tx_id = client.send_transaction(signed_txn)
        print(f"✓ Transaction ID: {tx_id}")
        
        # Wait for confirmation
        print("⏳ Waiting for confirmation...")
        confirmed_txn = transaction.wait_for_confirmation(client, tx_id, 4)
        
        app_id = confirmed_txn["application-index"]
        print(f"\n🎉 Smart contract deployed successfully!")
        print(f"📋 Application ID: {app_id}")
        print(f"\n✅ Update your .env files:")
        print(f"   backend/.env: ALGORAND_APP_ID={app_id}")
        print(f"   frontend/.env.local: NEXT_PUBLIC_ALGORAND_APP_ID={app_id}")
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")


if __name__ == "__main__":
    main()
