from datetime import datetime
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from models.claim_model import ClaimModel
from models.policy_model import PolicyModel
from services.ipfs_service import upload_file_to_ipfs
from services.algorand_service import submit_claim_to_chain
from utils.ids import generate_readable_id
from utils.serializers import serialize_doc


def submit_claim():
    user_id = get_jwt_identity()
    policy_id = request.form.get("policyId")
    doc_file = request.files.get("document")

    if not policy_id:
        return jsonify({"message": "policyId is required"}), 400

    policy = PolicyModel.find_by_policy_id(policy_id)
    if not policy:
        return jsonify({"message": "Policy not found"}), 404

    ipfs_hash = upload_file_to_ipfs(doc_file) if doc_file else None
    reason = request.form.get("reason", "")
    
    # Get amount from form, validate it
    try:
        amount = float(request.form.get("amount", 0))
        if amount <= 0:
            return jsonify({"message": "Claim amount must be greater than 0"}), 400
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid claim amount"}), 400

    claim = {
        "claimId": generate_readable_id("CLM"),
        "policyId": policy_id,
        "userId": user_id,
        "documents": [ipfs_hash] if ipfs_hash else [],
        "status": "pending",  # Changed from 'submitted' to 'pending' for better UI compatibility
        "reason": reason,
        "description": reason,  # Alias for frontend compatibility
        "amount": amount,
        "submittedAt": datetime.utcnow().isoformat() + "Z",
    }

    ClaimModel.create(claim)
    PolicyModel.collection().update_one({"policyId": policy_id}, {"$set": {"claimStatus": "pending"}})
    
    # Submit to blockchain
    blockchain_result = submit_claim_to_chain(claim["claimId"], policy_id)
    
    PolicyModel.collection().database.notifications.insert_one(
        {
            "userId": user_id,
            "type": "claim_submitted",
            "message": f"Claim {claim['claimId']} submitted for policy {policy_id}.",
            "isRead": False,
            "meta": {"claimId": claim["claimId"], "policyId": policy_id},
        }
    )

    return jsonify({
        "message": "Claim submitted", 
        "claim": serialize_doc(claim),
        "blockchain": blockchain_result
    }), 201


def claim_status(claim_id):
    claim = ClaimModel.find_by_claim_id(claim_id)
    if not claim:
        return jsonify({"message": "Claim not found"}), 404
    return jsonify(serialize_doc(claim)), 200
