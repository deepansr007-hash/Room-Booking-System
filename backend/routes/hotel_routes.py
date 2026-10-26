from flask import Blueprint, request, jsonify
from backend.models.hotel_model import HotelModel
from backend.models.room_model import RoomModel
from backend.utils.validators import (
    validate_required_fields,
    token_required,
    admin_required
)

hotel_bp = Blueprint("hotels", __name__, url_prefix="/api/hotels")

@hotel_bp.route("", methods=["GET"])
def list_hotels():
    city = request.args.get("city")
    min_rating = request.args.get("min_rating", type=float)
    query = request.args.get("q")

    hotels = HotelModel.find_all(city=city, min_rating=min_rating, query=query)
    
    # Attach minimum room price for quick hotel browsing
    results = []
    for h in hotels:
        h_copy = dict(h)
        rooms = RoomModel.find_by_hotel(h["id"])
        if rooms:
            h_copy["starting_price"] = min(r.get("price_per_night", 0) for r in rooms)
            h_copy["total_rooms"] = len(rooms)
        else:
            h_copy["starting_price"] = 0
            h_copy["total_rooms"] = 0
        results.append(h_copy)

    return jsonify({
        "success": True,
        "count": len(results),
        "hotels": results
    }), 200

@hotel_bp.route("/<hotel_id>", methods=["GET"])
def get_hotel(hotel_id):
    hotel = HotelModel.find_by_id(hotel_id)
    if not hotel:
        return jsonify({"success": False, "message": f"Hotel '{hotel_id}' not found."}), 404

    rooms = RoomModel.find_by_hotel(hotel_id)
    response_data = dict(hotel)
    response_data["rooms"] = rooms

    return jsonify({
        "success": True,
        "hotel": response_data
    }), 200

@hotel_bp.route("", methods=["POST"])
@token_required
@admin_required
def create_hotel(current_user):
    data = request.get_json() or {}
    valid, err = validate_required_fields(data, ["name", "city", "address", "description"])
    if not valid:
        return jsonify({"success": False, "message": err}), 400

    hotel = HotelModel.create(data)
    return jsonify({
        "success": True,
        "message": "Hotel created successfully.",
        "hotel": hotel
    }), 201

@hotel_bp.route("/<hotel_id>", methods=["PUT"])
@token_required
@admin_required
def update_hotel(current_user, hotel_id):
    hotel = HotelModel.find_by_id(hotel_id)
    if not hotel:
        return jsonify({"success": False, "message": "Hotel not found."}), 404

    data = request.get_json() or {}
    updated = HotelModel.update(hotel_id, data)
    return jsonify({
        "success": True,
        "message": "Hotel updated successfully.",
        "hotel": updated
    }), 200

@hotel_bp.route("/<hotel_id>", methods=["DELETE"])
@token_required
@admin_required
def delete_hotel(current_user, hotel_id):
    hotel = HotelModel.find_by_id(hotel_id)
    if not hotel:
        return jsonify({"success": False, "message": "Hotel not found."}), 404

    HotelModel.delete(hotel_id)
    return jsonify({
        "success": True,
        "message": "Hotel deleted successfully."
    }), 200
