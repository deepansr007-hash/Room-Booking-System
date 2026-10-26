import datetime
from backend.models.room_model import RoomModel
from backend.models.hotel_model import HotelModel
from backend.models.booking_model import BookingModel
from backend.utils.validators import validate_booking_dates

PROMO_CODES = {
    "LUXURY10": {"type": "percent", "value": 0.10, "min_nights": 1},
    "WELCOME50": {"type": "flat", "value": 50.0, "min_nights": 2},
    "SUMMER20": {"type": "percent", "value": 0.20, "min_nights": 3}
}

class BookingService:
    @staticmethod
    def calculate_price(room: dict, check_in_str: str, check_out_str: str, promo_code: str = None) -> dict:
        is_valid, err, d_in, d_out = validate_booking_dates(check_in_str, check_out_str)
        if not is_valid:
            raise ValueError(err)

        total_nights = (d_out - d_in).days
        price_per_night = float(room.get("price_per_night", 0.0))
        subtotal = round(price_per_night * total_nights, 2)
        
        # 12% standard luxury tax & services
        tax_rate = 0.12
        tax_amount = round(subtotal * tax_rate, 2)

        # Promo discount
        discount_amount = 0.0
        applied_promo = None
        if promo_code:
            code = promo_code.strip().upper()
            if code in PROMO_CODES:
                promo_info = PROMO_CODES[code]
                if total_nights >= promo_info["min_nights"]:
                    if promo_info["type"] == "percent":
                        discount_amount = round(subtotal * promo_info["value"], 2)
                    elif promo_info["type"] == "flat":
                        discount_amount = min(subtotal, promo_info["value"])
                    applied_promo = code

        total_amount = max(0.0, round(subtotal + tax_amount - discount_amount, 2))

        return {
            "total_nights": total_nights,
            "price_per_night": price_per_night,
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "tax_rate_percent": int(tax_rate * 100),
            "discount_amount": discount_amount,
            "applied_promo": applied_promo,
            "total_amount": total_amount
        }

    @staticmethod
    def check_availability(room_id: str, check_in_str: str, check_out_str: str) -> dict:
        room = RoomModel.find_by_id(room_id)
        if not room:
            return {"available": False, "reason": "Room not found."}
        
        if not room.get("is_available", True):
            return {"available": False, "reason": "Room is currently under maintenance."}

        overlapping = BookingModel.find_overlapping(room_id, check_in_str, check_out_str)
        if overlapping:
            return {
                "available": False,
                "reason": "Room is already reserved for the selected dates.",
                "conflicts": [
                    {"check_in": b.get("check_in"), "check_out": b.get("check_out")}
                    for b in overlapping
                ]
            }

        return {"available": True, "reason": "Room is available."}

    @staticmethod
    def create_reservation(user_id: str, data: dict) -> dict:
        room_id = data.get("room_id")
        check_in = data.get("check_in")
        check_out = data.get("check_out")
        num_guests = int(data.get("num_guests", 1))
        special_requests = data.get("special_requests", "")
        promo_code = data.get("promo_code", "")

        room = RoomModel.find_by_id(room_id)
        if not room:
            raise ValueError(f"Room with id '{room_id}' not found.")

        hotel = HotelModel.find_by_id(room.get("hotel_id"))
        if not hotel:
            raise ValueError("Associated hotel not found.")

        if num_guests > room.get("capacity", 2):
            raise ValueError(f"Guest count exceeds room maximum capacity of {room.get('capacity')}.")

        avail = BookingService.check_availability(room_id, check_in, check_out)
        if not avail["available"]:
            raise ValueError(avail["reason"])

        pricing = BookingService.calculate_price(room, check_in, check_out, promo_code)

        booking_data = {
            "user_id": user_id,
            "hotel_id": hotel["id"],
            "room_id": room["id"],
            "check_in": check_in,
            "check_out": check_out,
            "num_guests": num_guests,
            "total_nights": pricing["total_nights"],
            "price_per_night": pricing["price_per_night"],
            "tax_amount": pricing["tax_amount"],
            "discount_amount": pricing["discount_amount"],
            "total_amount": pricing["total_amount"],
            "special_requests": special_requests,
            "status": "pending"
        }

        booking = BookingModel.create(booking_data)
        booking["hotel"] = hotel
        booking["room"] = room
        return booking

    @staticmethod
    def cancel_reservation(booking_id: str, user_id: str, is_admin: bool = False) -> dict:
        booking = BookingModel.find_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found.")

        if not is_admin and booking.get("user_id") != user_id:
            raise PermissionError("Access denied. You cannot cancel someone else's booking.")

        if booking.get("status") == "cancelled":
            raise ValueError("Booking is already cancelled.")

        updated = BookingModel.update_status(booking_id, "cancelled")
        return updated
