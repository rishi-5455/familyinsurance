from flask import request, jsonify

from models.user_model import UserModel
from models.policy_model import PolicyModel
from models.claim_model import ClaimModel
from services.algorand_service import submit_claim_to_chain, approve_claim_on_chain
from utils.ids import generate_readable_id
from utils.serializers import serialize_doc


def create_policy_template():
    data = request.get_json() or {}
    required = ["name", "coverage", "durationMonths"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"message": f"Missing fields: {', '.join(missing)}"}), 400

    # Validate numeric fields
    try:
        coverage = float(data["coverage"])
        duration = int(data["durationMonths"])
    except (ValueError, TypeError) as e:
        return jsonify({"message": f"Invalid number format: {str(e)}"}), 400

    template = {
        "templateId": generate_readable_id("TPL"),
        "name": data["name"],
        "coverage": coverage,
        "durationMonths": duration,
        "description": data.get("description", ""),
        "status": "published",
    }

    PolicyModel.collection().database.policy_templates.insert_one(template)
    return jsonify({"message": "Policy template created", "template": serialize_doc(template)}), 201


def get_users():
    users = UserModel.list_all()
    return jsonify([serialize_doc(u) for u in users]), 200


def get_all_policies():
    policies = PolicyModel.list_all()
    return jsonify([serialize_doc(p) for p in policies]), 200


def get_all_templates():
    """Get all policy templates created by admin"""
    templates = list(PolicyModel.collection().database.policy_templates.find({}))
    return jsonify([serialize_doc(t) for t in templates]), 200


def get_all_claims():
    claims = ClaimModel.list_all()
    return jsonify([serialize_doc(c) for c in claims]), 200


def approve_claim():
    data = request.get_json() or {}
    claim_id = data.get("claimId")
    action = data.get("action", "approve")

    if not claim_id:
        return jsonify({"message": "claimId is required"}), 400

    claim = ClaimModel.find_by_claim_id(claim_id)
    if not claim:
        return jsonify({"message": "Claim not found"}), 404

    next_status = "approved" if action == "approve" else "rejected"
    ClaimModel.update_status(claim_id, next_status)

    PolicyModel.update_status(claim["policyId"], "active")
    
    # Submit approval/rejection to blockchain
    blockchain_result = approve_claim_on_chain(claim_id, claim["policyId"], action == "approve")
    
    PolicyModel.collection().database.notifications.insert_one(
        {
            "userId": claim["userId"],
            "type": "claim_status",
            "message": f"Claim {claim_id} was {next_status}.",
            "isRead": False,
            "meta": {"claimId": claim_id, "status": next_status},
        }
    )
    
    return jsonify({
        "message": f"Claim {next_status}", 
        "claimId": claim_id,
        "blockchain": blockchain_result
    }), 200


def get_analytics():
    user_count = UserModel.collection().count_documents({})
    policy_count = PolicyModel.collection().count_documents({})
    claim_count = ClaimModel.collection().count_documents({})
    approved_claims = ClaimModel.collection().count_documents({"status": "approved"})
    template_count = PolicyModel.collection().database.policy_templates.count_documents({})

    return jsonify(
        {
            "users": user_count,
            "policies": policy_count,
            "claims": claim_count,
            "approvedClaims": approved_claims,
            "templates": template_count,
        }
    ), 200


def clear_test_data():
    """Clear all test data from database (USE WITH CAUTION!)"""
    # Clear policies, claims, and notifications (keep users)
    PolicyModel.collection().delete_many({})
    ClaimModel.collection().delete_many({})
    PolicyModel.collection().database.policy_templates.delete_many({})
    PolicyModel.collection().database.notifications.delete_many({})
    
    return jsonify({
        "message": "Test data cleared successfully",
        "cleared": ["policies", "claims", "templates", "notifications"]
    }), 200
