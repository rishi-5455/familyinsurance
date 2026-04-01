from flask import Blueprint
from flask_jwt_extended import jwt_required

from controllers.admin_controller import (
    create_policy_template,
    get_users,
    get_all_policies,
    get_all_templates,
    get_all_claims,
    approve_claim,
    get_analytics,
    clear_test_data,
)
from utils.auth import role_required

admin_bp = Blueprint("admin", __name__)

admin_bp.post("/create-policy")(jwt_required()(role_required("admin")(create_policy_template)))
admin_bp.get("/users")(jwt_required()(role_required("admin")(get_users)))
admin_bp.get("/all-policies")(jwt_required()(role_required("admin")(get_all_policies)))
admin_bp.get("/all-templates")(jwt_required()(role_required("admin")(get_all_templates)))
admin_bp.get("/all-claims")(jwt_required()(role_required("admin")(get_all_claims)))
admin_bp.post("/approve-claim")(jwt_required()(role_required("admin")(approve_claim)))
admin_bp.get("/analytics")(jwt_required()(role_required("admin")(get_analytics)))
admin_bp.delete("/clear-test-data")(jwt_required()(role_required("admin")(clear_test_data)))
