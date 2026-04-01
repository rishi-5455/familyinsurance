from datetime import datetime, timedelta
from bson import ObjectId
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from models.user_model import UserModel
from models.policy_model import PolicyModel
from models.claim_model import ClaimModel
from services.ipfs_service import upload_file_to_ipfs
from services.algorand_service import sync_policy_to_chain
from utils.ids import generate_readable_id
from utils.serializers import serialize_doc


def get_profile():
    user_id = get_jwt_identity()
    user = UserModel.collection().find_one({"_id": ObjectId(user_id)}, {"password": 0})
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(serialize_doc(user)), 200


def add_family_member():
    user_id = get_jwt_identity()
    payload = request.get_json() or {}

    if not payload.get("name"):
        return jsonify({"message": "Family member name is required"}), 400

    # Validate age if provided
    age = payload.get("age")
    if age is not None:
        try:
            age = int(age)
            if age < 0 or age > 150:
                return jsonify({"message": "Invalid age value"}), 400
        except (ValueError, TypeError):
            return jsonify({"message": "Age must be a valid number"}), 400

    UserModel.collection().update_one(
        {"_id": ObjectId(user_id)},
        {
            "$push": {
                "familyMembers": {
                    "name": payload["name"],
                    "age": age,
                    "relation": payload.get("relation", "")
                }
            }
        },
    )

    return jsonify({"message": "Family member added"}), 200


def get_policies():
    user_id = get_jwt_identity()
    policies = PolicyModel.list_by_user(user_id)
    return jsonify([serialize_doc(p) for p in policies]), 200


def buy_policy():
    user_id = get_jwt_identity()

    form_data = request.form.to_dict()
    policy_file = request.files.get("document")
    ipfs_hash = upload_file_to_ipfs(policy_file) if policy_file else None

    # Validate and parse numeric fields
    try:
        coverage = float(form_data.get("coverage", 0))
        expiry_months = int(form_data.get("durationMonths", 12))
        family_members = __import__("json").loads(form_data.get("familyMembers", "[]"))
    except (ValueError, TypeError) as e:
        return jsonify({"message": f"Invalid input format: {str(e)}"}), 400

    if coverage <= 0:
        return jsonify({"message": "Coverage must be greater than 0"}), 400

    policy_id = generate_readable_id("POL")

    policy = {
        "policyId": policy_id,
        "userId": user_id,
        "familyMembers": family_members,
        "coverage": coverage,
        "expiry": (datetime.utcnow() + timedelta(days=30 * expiry_months)).isoformat() + "Z",
        "status": "active",
        "walletAddress": form_data.get("walletAddress", ""),
        "ipfsHash": ipfs_hash,
        "claimStatus": "none",
    }

    PolicyModel.create(policy)
    PolicyModel.collection().database.notifications.insert_one(
        {
            "userId": user_id,
            "type": "policy_created",
            "message": f"Policy {policy_id} purchased successfully.",
            "isRead": False,
            "meta": {"policyId": policy_id, "expiry": policy["expiry"]},
        }
    )
    chain_status = sync_policy_to_chain(policy)

    return jsonify({"message": "Policy purchased", "policy": serialize_doc(policy), "blockchain": chain_status}), 201


def link_wallet():
    user_id = get_jwt_identity()
    payload = request.get_json() or {}
    wallet_address = payload.get("walletAddress", "")
    if not wallet_address:
        return jsonify({"message": "walletAddress is required"}), 400

    UserModel.collection().update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"walletAddress": wallet_address}},
    )
    return jsonify({"message": "Wallet linked", "walletAddress": wallet_address}), 200


def get_notifications():
    user_id = get_jwt_identity()
    items = list(
        PolicyModel.collection().database.notifications.find(
            {"userId": user_id},
            {"userId": 0},
        )
    )
    return jsonify([serialize_doc(item) for item in items]), 200
