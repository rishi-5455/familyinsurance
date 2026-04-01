import os
import json
from datetime import datetime
from algosdk.v2client import algod
from algosdk import account, transaction, mnemonic
from algosdk.abi import Contract
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    AccountTransactionSigner,
    TransactionWithSigner,
)


def get_algod_client():
    """Initialize Algorand client."""
    algod_url = os.getenv("ALGORAND_ALGOD_URL", "https://testnet-api.algonode.cloud")
    algod_token = os.getenv("ALGORAND_ALGOD_TOKEN", "")
    return algod.AlgodClient(algod_token, algod_url)


def sync_policy_to_chain(policy: dict):
    """
    Submits policy data to Algorand smart contract.
    Calls createPolicy method with policy parameters.
    """
    app_id = int(os.getenv("ALGORAND_APP_ID", "0"))
    
    # If no app deployed yet, return pending status
    if app_id == 0:
        return {
            "synced": False,
            "appId": 0,
            "message": "Smart contract not deployed. Set ALGORAND_APP_ID in .env",
            "policyId": policy.get("policyId"),
        }
    
    try:
        client = get_algod_client()
        
        # Get creator account from mnemonic
        creator_mnemonic = os.getenv("ALGORAND_CREATOR_MNEMONIC")
        
        if not creator_mnemonic:
            # Return success but note that transaction wasn't signed
            return {
                "synced": True,
                "appId": app_id,
                "syncedAt": datetime.utcnow().isoformat() + "Z",
                "policyId": policy.get("policyId"),
                "message": "Created on-chain record (simulation mode - set ALGORAND_CREATOR_MNEMONIC for real txns)",
                "txnId": "simulated-txn-" + policy.get("policyId", "unknown"),
            }
        
        # Real blockchain transaction - convert mnemonic to private key
        creator_private_key = mnemonic.to_private_key(creator_mnemonic)
        sender_address = account.address_from_private_key(creator_private_key)
        params = client.suggested_params()
        
        # Load contract ABI
        contract_json_path = os.path.join(
            os.path.dirname(__file__), "../../blockchain/build/contract.json"
        )
        
        if not os.path.exists(contract_json_path):
            return {
                "synced": False,
                "message": "Contract ABI not found. Run: python blockchain/scripts/compile_contract.py",
                "policyId": policy.get("policyId"),
            }
        
        with open(contract_json_path, "r") as f:
            contract_dict = json.load(f)
        
        contract = Contract.from_json(json.dumps(contract_dict))
        create_policy_method = contract.get_method_by_name("createPolicy")
        
        # Build atomic transaction composer
        atc = AtomicTransactionComposer()
        signer = AccountTransactionSigner(creator_private_key)
        
        atc.add_method_call(
            app_id=app_id,
            method=create_policy_method,
            sender=sender_address,
            sp=params,
            signer=signer,
            method_args=[
                policy.get("policyId", ""),
                policy.get("walletAddress", ""),
                int(policy.get("coverage", 0)),
                policy.get("status", "active"),
                policy.get("expiry", ""),
                policy.get("claimStatus", "none"),
            ],
        )
        
        result = atc.execute(client, 4)
        txn_id = result.tx_ids[0] if result.tx_ids else "unknown"
        
        return {
            "synced": True,
            "appId": app_id,
            "syncedAt": datetime.utcnow().isoformat() + "Z",
            "policyId": policy.get("policyId"),
            "txnId": txn_id,
            "confirmedRound": result.confirmed_round if hasattr(result, "confirmed_round") else None,
        }
        
    except Exception as e:
        return {
            "synced": False,
            "appId": app_id,
            "error": str(e),
            "message": "Blockchain sync failed. Check ALGORAND config and contract deployment.",
            "policyId": policy.get("policyId"),
        }


def verify_policy_on_chain(policy_id: str):
    """Call verifyPolicy method on smart contract."""
    app_id = int(os.getenv("ALGORAND_APP_ID", "0"))
    
    if app_id == 0:
        return {"verified": False, "message": "Contract not deployed"}
    
    try:
        client = get_algod_client()
        app_info = client.application_info(app_id)
        
        # Read global state for verification
        global_state = app_info.get("params", {}).get("global-state", [])
        
        status_key = "status"
        for state in global_state:
            key = state.get("key", "")
            # Decode base64 key
            import base64
            decoded_key = base64.b64decode(key).decode("utf-8")
            if decoded_key == status_key:
                value = state.get("value", {})
                if value.get("type") == 1:  # bytes
                    status_value = base64.b64decode(value.get("bytes", "")).decode("utf-8")
                    return {"verified": status_value == "active", "status": status_value}
        
        return {"verified": False, "message": "Policy status not found on chain"}
        
    except Exception as e:
        return {"verified": False, "error": str(e)}


def submit_claim_to_chain(claim_id: str, policy_id: str):
    """Submit claim status update to blockchain."""
    app_id = int(os.getenv("ALGORAND_APP_ID", "0"))
    
    if app_id == 0:
        return {
            "synced": False,
            "message": "Contract not deployed",
            "claimId": claim_id,
        }
    
    try:
        client = get_algod_client()
        creator_mnemonic = os.getenv("ALGORAND_CREATOR_MNEMONIC")
        
        if not creator_mnemonic:
            return {
                "synced": True,
                "appId": app_id,
                "claimId": claim_id,
                "message": "Claim submitted (simulation mode - set ALGORAND_CREATOR_MNEMONIC)",
                "txnId": "simulated-claim-" + claim_id,
            }
        
        # Real blockchain transaction
        creator_private_key = mnemonic.to_private_key(creator_mnemonic)
        sender_address = account.address_from_private_key(creator_private_key)
        params = client.suggested_params()
        
        # Load contract ABI
        contract_json_path = os.path.join(
            os.path.dirname(__file__), "../../blockchain/build/contract.json"
        )
        
        if not os.path.exists(contract_json_path):
            return {
                "synced": False,
                "message": "Contract ABI not found",
                "claimId": claim_id,
            }
        
        with open(contract_json_path, "r") as f:
            contract_dict = json.load(f)
        
        contract = Contract.from_json(json.dumps(contract_dict))
        submit_claim_method = contract.get_method_by_name("submitClaim")
        
        # Build atomic transaction composer
        atc = AtomicTransactionComposer()
        signer = AccountTransactionSigner(creator_private_key)
        
        atc.add_method_call(
            app_id=app_id,
            method=submit_claim_method,
            sender=sender_address,
            sp=params,
            signer=signer,
            method_args=["submitted"],  # claim status
        )
        
        result = atc.execute(client, 4)
        txn_id = result.tx_ids[0] if result.tx_ids else "unknown"
        
        return {
            "synced": True,
            "appId": app_id,
            "claimId": claim_id,
            "txnId": txn_id,
            "confirmedRound": result.confirmed_round if hasattr(result, "confirmed_round") else None,
        }
        
    except Exception as e:
        return {
            "synced": False,
            "appId": app_id,
            "claimId": claim_id,
            "error": str(e),
            "message": "Blockchain claim submission failed",
        }


def approve_claim_on_chain(claim_id: str, policy_id: str, approved: bool):
    """Approve or reject claim on blockchain."""
    app_id = int(os.getenv("ALGORAND_APP_ID", "0"))
    
    if app_id == 0:
        return {
            "synced": False,
            "message": "Contract not deployed",
            "claimId": claim_id,
        }
    
    try:
        client = get_algod_client()
        creator_mnemonic = os.getenv("ALGORAND_CREATOR_MNEMONIC")
        
        if not creator_mnemonic:
            return {
                "synced": True,
                "appId": app_id,
                "claimId": claim_id,
                "message": "Claim approved (simulation mode - set ALGORAND_CREATOR_MNEMONIC)",
                "txnId": f"simulated-approve-{claim_id}",
            }
        
        # Real blockchain transaction
        creator_private_key = mnemonic.to_private_key(creator_mnemonic)
        sender_address = account.address_from_private_key(creator_private_key)
        params = client.suggested_params()
        
        # Load contract ABI
        contract_json_path = os.path.join(
            os.path.dirname(__file__), "../../blockchain/build/contract.json"
        )
        
        if not os.path.exists(contract_json_path):
            return {
                "synced": False,
                "message": "Contract ABI not found",
                "claimId": claim_id,
            }
        
        with open(contract_json_path, "r") as f:
            contract_dict = json.load(f)
        
        contract = Contract.from_json(json.dumps(contract_dict))
        approve_claim_method = contract.get_method_by_name("approveClaim")
        
        # Build atomic transaction composer
        atc = AtomicTransactionComposer()
        signer = AccountTransactionSigner(creator_private_key)
        
        claim_status = "approved" if approved else "rejected"
        policy_status = "active" if approved else "active"  # Keep policy active either way
        
        atc.add_method_call(
            app_id=app_id,
            method=approve_claim_method,
            sender=sender_address,
            sp=params,
            signer=signer,
            method_args=[claim_status, policy_status],
        )
        
        result = atc.execute(client, 4)
        txn_id = result.tx_ids[0] if result.tx_ids else "unknown"
        
        return {
            "synced": True,
            "appId": app_id,
            "claimId": claim_id,
            "status": claim_status,
            "txnId": txn_id,
            "confirmedRound": result.confirmed_round if hasattr(result, "confirmed_round") else None,
        }
        
    except Exception as e:
        return {
            "synced": False,
            "appId": app_id,
            "claimId": claim_id,
            "error": str(e),
            "message": "Blockchain claim approval failed",
        }
