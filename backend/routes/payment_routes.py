from flask import Blueprint, request, jsonify
from backend.services.payment_service import PaymentService
from backend.models.payment_model import PaymentModel
from backend.utils.validators import (
    validate_required_fields,
    token_required
)

payment_bp = Blueprint("payments", __name__, url_prefix="/api/payments")

@payment_bp.route("/process", methods=["POST"])
@token_required
def process_payment(current_user):
    data = request.get_json() or {}
    valid, err = validate_required_fields(data, ["booking_id", "payment_method"])
    if not valid:
        return jsonify({"success": False, "message": err}), 400

    booking_id = data.get("booking_id")
    payment_method = data.get("payment_method")
    details = data.get("details", {})

    try:
        result = PaymentService.process_payment(
            booking_id=booking_id,
            user_id=current_user["user_id"],
            payment_method=payment_method,
            details=details
        )
        return jsonify(result), 200
    except PermissionError as e:
        return jsonify({"success": False, "message": str(e)}), 403
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": f"Payment processing error: {str(e)}"}), 500

@payment_bp.route("/receipt/<payment_id>", methods=["GET"])
@token_required
def get_receipt(current_user, payment_id):
    try:
        receipt = PaymentService.get_receipt(payment_id)
        return jsonify({
            "success": True,
            "receipt": receipt
        }), 200
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 404

@payment_bp.route("/booking/<booking_id>", methods=["GET"])
@token_required
def get_booking_payments(current_user, booking_id):
    payments = PaymentModel.find_by_booking(booking_id)
    return jsonify({
        "success": True,
        "payments": payments
    }), 200
