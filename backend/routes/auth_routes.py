from flask import Blueprint, request, jsonify
from backend.models.user_model import UserModel
from backend.utils.validators import (
    validate_email,
    validate_password,
    validate_phone,
    validate_required_fields,
    generate_jwt_token,
    token_required,
    admin_required
)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    
    valid, err = validate_required_fields(data, ["name", "email", "password", "phone"])
    if not valid:
        return jsonify({"success": False, "message": err}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    role = data.get("role", "guest")

    if not validate_email(email):
        return jsonify({"success": False, "message": "Invalid email address format."}), 400

    pwd_valid, pwd_err = validate_password(password)
    if not pwd_valid:
        return jsonify({"success": False, "message": pwd_err}), 400

    if not validate_phone(phone):
        return jsonify({"success": False, "message": "Invalid phone number format."}), 400

    existing_user = UserModel.find_by_email(email)
    if existing_user:
        return jsonify({"success": False, "message": "An account with this email already exists."}), 409

    user = UserModel.create(name, email, password, phone, role)
    token = generate_jwt_token(user["id"], user["email"], user["role"])

    return jsonify({
        "success": True,
        "message": "User registered successfully.",
        "token": token,
        "user": user
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    
    valid, err = validate_required_fields(data, ["email", "password"])
    if not valid:
        return jsonify({"success": False, "message": err}), 400

    email = data.get("email")
    password = data.get("password")

    user = UserModel.find_by_email(email)
    if not user:
        return jsonify({"success": False, "message": "Invalid email or password."}), 401

    if not UserModel.verify_password(user.get("password_hash"), password):
        return jsonify({"success": False, "message": "Invalid email or password."}), 401

    token = generate_jwt_token(user["id"], user["email"], user["role"])
    user_data = UserModel.to_dict(user)

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "token": token,
        "user": user_data
    }), 200

@auth_bp.route("/me", methods=["GET"])
@token_required
def get_current_user(current_user):
    user = UserModel.find_by_id(current_user["user_id"])
    if not user:
        return jsonify({"success": False, "message": "User account no longer exists."}), 404
    return jsonify({
        "success": True,
        "user": UserModel.to_dict(user)
    }), 200

@auth_bp.route("/users", methods=["GET"])
@token_required
@admin_required
def list_users(current_user):
    users = UserModel.get_all()
    return jsonify({
        "success": True,
        "count": len(users),
        "users": users
    }), 200
