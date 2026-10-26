from flask import Blueprint, request, jsonify
from backend.models.booking_model import BookingModel
from backend.models.hotel_model import HotelModel
from backend.models.room_model import RoomModel
from backend.models.payment_model import PaymentModel
from backend.services.booking_service import BookingService
from backend.utils.validators import (
    validate_required_fields,
    token_required,
    admin_required
)

booking_bp = Blueprint("bookings", __name__, url_prefix="/api/bookings")

@booking_bp.route("/quote", methods=["POST"])
def get_quote():
    data = request.get_json() or {}
    valid, err = validate_required_fields(data, ["room_id", "check_in", "check_out"])
    if not valid:
        return jsonify({"success": False, "message": err}), 400

    room = RoomModel.find_by_id(data.get("room_id"))
    if not room:
        return jsonify({"success": False, "message": "Room not found."}), 404

    try:
        pricing = BookingService.calculate_price(
            room,
            data.get("check_in"),
            data.get("check_out"),
            data.get("promo_code")
        )
        return jsonify({
            "success": True,
            "pricing": pricing
        }), 200
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

@booking_bp.route("", methods=["POST"])
@token_required
def create_booking(current_user):
    data = request.get_json() or {}
    valid, err = validate_required_fields(data, ["room_id", "check_in", "check_out"])
    if not valid:
        return jsonify({"success": False, "message": err}), 400

    try:
        booking = BookingService.create_reservation(current_user["user_id"], data)
        return jsonify({
            "success": True,
            "message": "Booking created. Please complete payment to confirm reservation.",
            "booking": booking
        }), 201
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

@booking_bp.route("/my-bookings", methods=["GET"])
@token_required
def get_my_bookings(current_user):
    user_bookings = BookingModel.find_by_user(current_user["user_id"])
    
    enriched = []
    for b in user_bookings:
        b_copy = dict(b)
        b_copy["hotel"] = HotelModel.find_by_id(b.get("hotel_id"))
        b_copy["room"] = RoomModel.find_by_id(b.get("room_id"))
        payments = PaymentModel.find_by_booking(b.get("id"))
        b_copy["payment"] = payments[0] if payments else None
        enriched.append(b_copy)

    # Sort newest first
    enriched.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return jsonify({
        "success": True,
        "count": len(enriched),
        "bookings": enriched
    }), 200

@booking_bp.route("/<booking_id>", methods=["GET"])
@token_required
def get_booking(current_user, booking_id):
    booking = BookingModel.find_by_id(booking_id)
    if not booking:
        return jsonify({"success": False, "message": "Booking not found."}), 404

    if current_user.get("role") != "admin" and booking.get("user_id") != current_user["user_id"]:
        return jsonify({"success": False, "message": "Unauthorized access to reservation."}), 403

    b_data = dict(booking)
    b_data["hotel"] = HotelModel.find_by_id(booking.get("hotel_id"))
    b_data["room"] = RoomModel.find_by_id(booking.get("room_id"))
    b_data["payments"] = PaymentModel.find_by_booking(booking_id)

    return jsonify({
        "success": True,
        "booking": b_data
    }), 200

@booking_bp.route("/<booking_id>/cancel", methods=["POST"])
@token_required
def cancel_booking(current_user, booking_id):
    is_admin = current_user.get("role") == "admin"
    try:
        updated = BookingService.cancel_reservation(booking_id, current_user["user_id"], is_admin=is_admin)
        return jsonify({
            "success": True,
            "message": "Booking successfully cancelled.",
            "booking": updated
        }), 200
    except PermissionError as e:
        return jsonify({"success": False, "message": str(e)}), 403
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

@booking_bp.route("", methods=["GET"])
@token_required
@admin_required
def list_all_bookings(current_user):
    all_bookings = BookingModel.find_all()
    enriched = []
    for b in all_bookings:
        b_copy = dict(b)
        b_copy["hotel"] = HotelModel.find_by_id(b.get("hotel_id"))
        b_copy["room"] = RoomModel.find_by_id(b.get("room_id"))
        enriched.append(b_copy)

    enriched.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return jsonify({
        "success": True,
        "count": len(enriched),
        "bookings": enriched
    }), 200
