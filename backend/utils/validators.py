import re
import uuid
import datetime
from functools import wraps
from flask import request, jsonify
import jwt
from backend.config import Config

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"
PHONE_REGEX = r"^\+?[0-9\s\-\(\)]{7,20}$"

def validate_email(email: str) -> bool:
    if not email or not isinstance(email, str):
        return False
    return bool(re.match(EMAIL_REGEX, email.strip()))

def validate_password(password: str) -> tuple[bool, str]:
    if not password or not isinstance(password, str):
        return False, "Password cannot be empty."
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""

def validate_phone(phone: str) -> bool:
    if not phone or not isinstance(phone, str):
        return False
    return bool(re.match(PHONE_REGEX, phone.strip()))

def validate_booking_dates(check_in_str: str, check_out_str: str) -> tuple[bool, str, datetime.date, datetime.date]:
    try:
        check_in = datetime.datetime.strptime(check_in_str, "%Y-%m-%d").date()
        check_out = datetime.datetime.strptime(check_out_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return False, "Dates must be in YYYY-MM-DD format.", None, None

    today = datetime.date.today()
    if check_in < today:
        return False, f"Check-in date cannot be in the past ({check_in} < {today}).", None, None
        
    if check_out <= check_in:
        return False, "Check-out date must be strictly after check-in date.", None, None

    return True, "", check_in, check_out

def validate_required_fields(data: dict, fields: list) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, "Invalid payload format. Expected JSON object."
    missing = [f for f in fields if f not in data or data[f] is None or data[f] == ""]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, ""

def generate_id(prefix: str = "item") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def generate_booking_code() -> str:
    return f"BK-{uuid.uuid4().int % 1000000:06d}"

def generate_transaction_id() -> str:
    return f"TXN_{uuid.uuid4().int % 10000000000:010d}"

def generate_jwt_token(user_id: str, email: str, role: str) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=Config.JWT_ACCESS_TOKEN_EXPIRES_HOURS),
        "iat": datetime.datetime.utcnow()
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")

def decode_jwt_token(token: str) -> dict:
    try:
        return jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ValueError("Authentication token has expired.")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid authentication token.")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header:
            return jsonify({"success": False, "message": "Missing Authorization header."}), 401
        
        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"success": False, "message": "Authorization header must be Bearer <token>."}), 401
        
        token = parts[1]
        try:
            current_user = decode_jwt_token(token)
        except ValueError as err:
            return jsonify({"success": False, "message": str(err)}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.get("role") != "admin":
            return jsonify({"success": False, "message": "Administrative privileges required."}), 403
        return f(current_user, *args, **kwargs)
    return decorated
