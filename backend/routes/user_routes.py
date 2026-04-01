from flask import Blueprint
from flask_jwt_extended import jwt_required

from controllers.user_controller import (
	get_profile,
	add_family_member,
	get_policies,
	buy_policy,
	link_wallet,
	get_notifications,
)
from utils.auth import role_required

user_bp = Blueprint("user", __name__)

user_bp.get("/profile")(jwt_required()(role_required("user", "admin", "verifier")(get_profile)))
user_bp.post("/family")(jwt_required()(role_required("user")(add_family_member)))
user_bp.get("/policies")(jwt_required()(role_required("user")(get_policies)))
user_bp.post("/buy-policy")(jwt_required()(role_required("user")(buy_policy)))
user_bp.post("/link-wallet")(jwt_required()(role_required("user")(link_wallet)))
user_bp.get("/notifications")(jwt_required()(role_required("user")(get_notifications)))
