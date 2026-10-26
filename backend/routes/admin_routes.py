from flask import Blueprint, request, jsonify
from backend.models.user_model import UserModel
from backend.models.booking_model import BookingModel
from backend.models.hotel_model import HotelModel
from backend.models.room_model import RoomModel
from backend.models.payment_model import PaymentModel
from backend.utils.validators import token_required, admin_required, validate_required_fields

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@admin_bp.route("/stats", methods=["GET"])
@token_required
@admin_required
def get_dashboard_stats(current_user):
    users = UserModel.get_all()
    bookings = BookingModel.find_all()
    hotels = HotelModel.find_all()
    rooms = RoomModel.find_all()

    confirmed_count = sum(1 for b in bookings if b.get("status") == "confirmed")
    pending_count = sum(1 for b in bookings if b.get("status") == "pending")
    cancelled_count = sum(1 for b in bookings if b.get("status") == "cancelled")
    
    total_revenue = sum(
        float(b.get("total_amount", 0.0))
        for b in bookings
        if b.get("status") in ["confirmed", "completed"]
    )

    return jsonify({
        "success": True,
        "stats": {
            "total_users": len(users),
            "total_guests": sum(1 for u in users if u.get("role") == "guest"),
            "total_admins": sum(1 for u in users if u.get("role") == "admin"),
            "total_bookings": len(bookings),
            "confirmed_bookings": confirmed_count,
            "pending_bookings": pending_count,
            "cancelled_bookings": cancelled_count,
            "total_revenue": round(total_revenue, 2),
            "total_hotels": len(hotels),
            "total_rooms": len(rooms)
        }
    }), 200

@admin_bp.route("/users", methods=["GET"])
@token_required
@admin_required
def get_all_users(current_user):
    users = UserModel.get_all()
    all_bookings = BookingModel.find_all()

    enriched_users = []
    for u in users:
        u_copy = dict(u)
        user_bookings = [b for b in all_bookings if b.get("user_id") == u["id"]]
        u_copy["total_bookings"] = len(user_bookings)
        u_copy["total_spent"] = sum(
            float(b.get("total_amount", 0.0))
            for b in user_bookings
            if b.get("status") in ["confirmed", "completed"]
        )
        enriched_users.append(u_copy)

    enriched_users.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return jsonify({
        "success": True,
        "count": len(enriched_users),
        "users": enriched_users
    }), 200

@admin_bp.route("/users/<user_id>/role", methods=["PUT"])
@token_required
@admin_required
def update_user_role(current_user, user_id):
    if user_id == current_user["user_id"]:
        return jsonify({"success": False, "message": "You cannot alter your own admin privileges."}), 400

    data = request.get_json() or {}
    new_role = data.get("role")
    if new_role not in ["guest", "admin"]:
        return jsonify({"success": False, "message": "Role must be 'guest' or 'admin'."}), 400

    updated = UserModel.update_role(user_id, new_role)
    if not updated:
        return jsonify({"success": False, "message": "User not found."}), 404

    return jsonify({
        "success": True,
        "message": f"User role updated to '{new_role}'.",
        "user": updated
    }), 200

@admin_bp.route("/users/<user_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_user(current_user, user_id):
    if user_id == current_user["user_id"]:
        return jsonify({"success": False, "message": "Cannot delete your own administrator account."}), 400

    target = UserModel.find_by_id(user_id)
    if not target:
        return jsonify({"success": False, "message": "User account does not exist."}), 404

    UserModel.delete(user_id)
    return jsonify({
        "success": True,
        "message": f"User '{target.get('name')}' ({target.get('email')}) deleted successfully."
    }), 200

@admin_bp.route("/bookings", methods=["GET"])
@token_required
@admin_required
def get_all_bookings(current_user):
    bookings = BookingModel.find_all()
    enriched = []

    for b in bookings:
        b_copy = dict(b)
        b_copy["user"] = UserModel.find_by_id(b.get("user_id"))
        b_copy["hotel"] = HotelModel.find_by_id(b.get("hotel_id"))
        b_copy["room"] = RoomModel.find_by_id(b.get("room_id"))
        payments = PaymentModel.find_by_booking(b.get("id"))
        b_copy["payment"] = payments[0] if payments else None
        enriched.append(b_copy)

    enriched.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return jsonify({
        "success": True,
        "count": len(enriched),
        "bookings": enriched
    }), 200

@admin_bp.route("/bookings/<booking_id>/status", methods=["PUT"])
@token_required
@admin_required
def update_booking_status(current_user, booking_id):
    data = request.get_json() or {}
    status = data.get("status")
    if status not in ["pending", "confirmed", "cancelled", "completed"]:
        return jsonify({"success": False, "message": "Invalid status value."}), 400

    updated = BookingModel.update_status(booking_id, status)
    if not updated:
        return jsonify({"success": False, "message": "Booking not found."}), 404

    return jsonify({
        "success": True,
        "message": f"Booking status updated to '{status}'.",
        "booking": updated
    }), 200

@admin_bp.route("/bookings/<booking_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_booking(current_user, booking_id):
    booking = BookingModel.find_by_id(booking_id)
    if not booking:
        return jsonify({"success": False, "message": "Booking not found."}), 404

    BookingModel.delete(booking_id)
    PaymentModel.delete_by_booking(booking_id)
    return jsonify({
        "success": True,
        "message": f"Booking ticket '{booking.get('booking_code', booking_id)}' deleted successfully."
    }), 200

@admin_bp.route("/hotels", methods=["POST"])
@token_required
@admin_required
def add_trip_place(current_user):
    data = request.get_json() or {}
    valid, err = validate_required_fields(data, ["name", "city", "address", "description"])
    if not valid:
        return jsonify({"success": False, "message": err}), 400

    hotel = HotelModel.create(data)
    
    # Auto-seed a default luxury suite for this new trip place so it is bookable
    room_data = {
        "hotel_id": hotel["id"],
        "room_number": f"{hotel['city'][:3].upper()}-101",
        "room_type": data.get("default_suite_name", "Deluxe Heritage Suite"),
        "price_per_night": float(data.get("starting_price", 250.0)),
        "capacity": int(data.get("capacity", 2)),
        "bed_type": "King Size Bed",
        "images": hotel.get("images", []),
        "features": ["Valley & Heritage Balcony", "Italian Marble Bath", "Rain Shower", "High-Speed WiFi"]
    }
    RoomModel.create(room_data)

    return jsonify({
        "success": True,
        "message": f"Trip place '{hotel['name']}' added to portfolio.",
        "hotel": hotel
    }), 201

@admin_bp.route("/rooms", methods=["GET"])
@token_required
@admin_required
def get_all_rooms(current_user):
    rooms = RoomModel.find_all()
    all_bookings = BookingModel.find_all()
    
    enriched = []
    for r in rooms:
        r_copy = dict(r)
        hotel = HotelModel.find_by_id(r.get("hotel_id"))
        if hotel:
            r_copy["hotel_name"] = hotel.get("name")
            r_copy["hotel_city"] = hotel.get("city")
        r_copy["active_bookings"] = sum(
            1 for b in all_bookings
            if b.get("room_id") == r["id"] and b.get("status") in ["confirmed", "pending"]
        )
        enriched.append(r_copy)

    enriched.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return jsonify({
        "success": True,
        "count": len(enriched),
        "rooms": enriched
    }), 200

@admin_bp.route("/rooms", methods=["POST"])
@token_required
@admin_required
def create_suite(current_user):
    data = request.get_json() or {}
    valid, err = validate_required_fields(data, ["hotel_id", "room_number", "room_type", "price_per_night"])
    if not valid:
        return jsonify({"success": False, "message": err}), 400

    hotel = HotelModel.find_by_id(data.get("hotel_id"))
    if not hotel:
        return jsonify({"success": False, "message": "Selected trip place/hotel does not exist."}), 404

    suite = RoomModel.create(data)
    return jsonify({
        "success": True,
        "message": f"Suite '{suite.get('room_type')}' created successfully.",
        "room": suite
    }), 201

@admin_bp.route("/rooms/<room_id>", methods=["PUT"])
@token_required
@admin_required
def update_suite(current_user, room_id):
    room = RoomModel.find_by_id(room_id)
    if not room:
        return jsonify({"success": False, "message": "Suite not found."}), 404

    data = request.get_json() or {}
    updated = RoomModel.update(room_id, data)
    return jsonify({
        "success": True,
        "message": "Suite details updated successfully.",
        "room": updated
    }), 200

@admin_bp.route("/rooms/<room_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_suite(current_user, room_id):
    room = RoomModel.find_by_id(room_id)
    if not room:
        return jsonify({"success": False, "message": "Suite not found."}), 404

    RoomModel.delete(room_id)
    return jsonify({
        "success": True,
        "message": f"Suite '{room.get('room_type', room_id)}' deleted successfully."
    }), 200

