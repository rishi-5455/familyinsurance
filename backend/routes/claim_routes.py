from flask import Blueprint
from flask_jwt_extended import jwt_required

from controllers.claim_controller import submit_claim, claim_status
from utils.auth import role_required

claim_bp = Blueprint("claims", __name__)

claim_bp.post("/submit-claim")(jwt_required()(role_required("user")(submit_claim)))
claim_bp.get("/claim-status/<string:claim_id>")(jwt_required()(role_required("user", "admin")(claim_status)))
