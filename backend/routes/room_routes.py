from flask import Blueprint, request, jsonify
from backend.models.room_model import RoomModel
from backend.models.hotel_model import HotelModel
from backend.services.booking_service import BookingService
from backend.utils.validators import (
    validate_required_fields,
    token_required,
    admin_required
)

room_bp = Blueprint("rooms", __name__, url_prefix="/api/rooms")

@room_bp.route("", methods=["GET"])
def list_rooms():
    hotel_id = request.args.get("hotel_id")
    max_price = request.args.get("max_price", type=float)
    room_type = request.args.get("room_type")
    capacity = request.args.get("capacity", type=int)

    if hotel_id:
        rooms = RoomModel.find_by_hotel(hotel_id)
        if max_price:
            rooms = [r for r in rooms if r.get("price_per_night", 0) <= max_price]
        if room_type and room_type.lower() != "all":
            rooms = [r for r in rooms if room_type.lower() in r.get("room_type", "").lower()]
        if capacity:
            rooms = [r for r in rooms if r.get("capacity", 0) >= capacity]
    else:
        rooms = RoomModel.find_all(max_price=max_price, room_type=room_type, capacity=capacity)

    # Attach hotel metadata for rich card presentation
    enhanced_rooms = []
    for r in rooms:
        r_copy = dict(r)
        hotel = HotelModel.find_by_id(r.get("hotel_id"))
        if hotel:
            r_copy["hotel_name"] = hotel.get("name")
            r_copy["hotel_city"] = hotel.get("city")
            r_copy["hotel_star_rating"] = hotel.get("star_rating")
        enhanced_rooms.append(r_copy)

    return jsonify({
        "success": True,
        "count": len(enhanced_rooms),
        "rooms": enhanced_rooms
    }), 200

@room_bp.route("/<room_id>", methods=["GET"])
def get_room(room_id):
    room = RoomModel.find_by_id(room_id)
    if not room:
        return jsonify({"success": False, "message": f"Room '{room_id}' not found."}), 404

    hotel = HotelModel.find_by_id(room.get("hotel_id"))
    data = dict(room)
    data["hotel"] = hotel

    return jsonify({
        "success": True,
        "room": data
    }), 200

@room_bp.route("/<room_id>/availability", methods=["GET"])
def check_room_availability(room_id):
    check_in = request.args.get("check_in")
    check_out = request.args.get("check_out")

    if not check_in or not check_out:
        return jsonify({
            "success": False,
            "message": "Both 'check_in' and 'check_out' query parameters are required."
        }), 400

    result = BookingService.check_availability(room_id, check_in, check_out)
    return jsonify({
        "success": True,
        **result
    }), 200

@room_bp.route("", methods=["POST"])
@token_required
@admin_required
def create_room(current_user):
    data = request.get_json() or {}
    valid, err = validate_required_fields(data, ["hotel_id", "room_number", "room_type", "price_per_night"])
    if not valid:
        return jsonify({"success": False, "message": err}), 400

    hotel = HotelModel.find_by_id(data.get("hotel_id"))
    if not hotel:
        return jsonify({"success": False, "message": "Specified hotel does not exist."}), 404

    room = RoomModel.create(data)
    return jsonify({
        "success": True,
        "message": "Room created successfully.",
        "room": room
    }), 201

@room_bp.route("/<room_id>", methods=["PUT"])
@token_required
@admin_required
def update_room(current_user, room_id):
    room = RoomModel.find_by_id(room_id)
    if not room:
        return jsonify({"success": False, "message": "Room not found."}), 404

    data = request.get_json() or {}
    updated = RoomModel.update(room_id, data)
    return jsonify({
        "success": True,
        "message": "Room updated successfully.",
        "room": updated
    }), 200

@room_bp.route("/<room_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_room(current_user, room_id):
    room = RoomModel.find_by_id(room_id)
    if not room:
        return jsonify({"success": False, "message": "Room not found."}), 404

    RoomModel.delete(room_id)
    return jsonify({
        "success": True,
        "message": "Room deleted successfully."
    }), 200
