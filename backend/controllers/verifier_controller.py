import io
import qrcode
from flask import jsonify, send_file

from models.policy_model import PolicyModel
from services.algorand_service import verify_policy_on_chain
from utils.serializers import serialize_doc


def verify_policy(policy_id):
    policy = PolicyModel.find_by_policy_id(policy_id)
    if not policy:
        return jsonify({"message": "Policy not found in database"}), 404
    
    # Verify on blockchain
    blockchain_verification = verify_policy_on_chain(policy_id)
    
    # Check both database and blockchain status
    db_verified = policy.get("status") == "active"
    blockchain_verified = blockchain_verification.get("verified", False)
    
    return jsonify({
        "verified": db_verified and blockchain_verified,
        "policy": serialize_doc(policy),
        "blockchainVerification": blockchain_verification,
        "databaseStatus": policy.get("status"),
    }), 200


def get_policy_qr(policy_id):
    policy = PolicyModel.find_by_policy_id(policy_id)
    if not policy:
        return jsonify({"message": "Policy not found"}), 404

    verification_url = f"verify://policy/{policy_id}"
    qr = qrcode.QRCode(version=1, box_size=8, border=4)
    qr.add_data(verification_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype="image/png")
