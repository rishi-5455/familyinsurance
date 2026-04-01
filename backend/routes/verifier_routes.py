from flask import Blueprint
from flask_jwt_extended import jwt_required

from controllers.verifier_controller import verify_policy, get_policy_qr
from utils.auth import role_required

verifier_bp = Blueprint("verifier", __name__)

verifier_bp.get("/verify-policy/<string:policy_id>")(jwt_required()(role_required("verifier", "admin")(verify_policy)))
verifier_bp.get("/policy-qr/<string:policy_id>")(jwt_required()(role_required("verifier", "admin", "user")(get_policy_qr)))
