from flask import request, jsonify
from flask_jwt_extended import create_access_token

from app import bcrypt
from models.user_model import UserModel
from utils.serializers import serialize_doc


ALLOWED_ROLES = {"admin", "user", "verifier"}


def register():
    data = request.get_json() or {}

    required_fields = ["name", "email", "password", "role"]
    missing = [f for f in required_fields if f not in data or not data.get(f)]
    if missing:
        return jsonify({"message": f"Missing fields: {', '.join(missing)}"}), 400

    if data["role"] not in ALLOWED_ROLES:
        return jsonify({"message": "Invalid role"}), 400

    existing = UserModel.find_by_email(data["email"])
    if existing:
        return jsonify({"message": "Email already registered"}), 409

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    result = UserModel.create(
        {
            "name": data["name"],
            "email": data["email"].lower(),
            "password": hashed_password,
            "role": data["role"],
            "walletAddress": data.get("walletAddress", ""),
        }
    )

    user = UserModel.collection().find_one({"_id": result.inserted_id}, {"password": 0})
    
    # Generate JWT token for immediate login after registration
    user_id = str(user["_id"])
    access_token = create_access_token(identity=user_id, additional_claims={"role": user["role"]})
    
    return jsonify({
        "message": "Registered successfully", 
        "user": serialize_doc(user),
        "access_token": access_token
    }), 201


def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = UserModel.find_by_email(email)
    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    user_id = str(user.get("_id"))
    access_token = create_access_token(identity=user_id, additional_claims={"role": user["role"]})

    payload = serialize_doc({k: v for k, v in user.items() if k != "password"})
    return jsonify({"message": "Login successful", "access_token": access_token, "user": payload}), 200
