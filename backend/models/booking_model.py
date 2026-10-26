import datetime
from backend.models.db_manager import db
from backend.utils.validators import generate_id, generate_booking_code

COLLECTION = "bookings"

class BookingModel:
    @staticmethod
    def create(data: dict) -> dict:
        booking_id = generate_id("bk")
        booking_code = generate_booking_code()
        now = datetime.datetime.utcnow().isoformat() + "Z"
        
        booking_doc = {
            "id": booking_id,
            "booking_code": booking_code,
            "user_id": data.get("user_id"),
            "hotel_id": data.get("hotel_id"),
            "room_id": data.get("room_id"),
            "check_in": data.get("check_in"),
            "check_out": data.get("check_out"),
            "num_guests": int(data.get("num_guests", 1)),
            "total_nights": int(data.get("total_nights", 1)),
            "price_per_night": float(data.get("price_per_night", 0.0)),
            "tax_amount": float(data.get("tax_amount", 0.0)),
            "discount_amount": float(data.get("discount_amount", 0.0)),
            "total_amount": float(data.get("total_amount", 0.0)),
            "special_requests": data.get("special_requests", ""),
            "status": data.get("status", "confirmed"),
            "created_at": now
        }
        
        db.insert(COLLECTION, booking_doc)
        return booking_doc

    @staticmethod
    def find_by_id(booking_id: str) -> dict | None:
        return db.find_one(COLLECTION, {"id": booking_id})

    @staticmethod
    def find_by_user(user_id: str) -> list[dict]:
        return db.find(COLLECTION, {"user_id": user_id})

    @staticmethod
    def find_all() -> list[dict]:
        return db.get_all(COLLECTION)

    @staticmethod
    def find_overlapping(room_id: str, check_in_str: str, check_out_str: str, exclude_booking_id: str = None) -> list[dict]:
        """
        Collision detection: returns active bookings that overlap with the requested dates.
        Overlap formula: NOT (existing_checkout <= new_checkin OR existing_checkin >= new_checkout)
        """
        all_bookings = db.find(COLLECTION, {"room_id": room_id})
        overlapping = []
        
        try:
            req_in = datetime.datetime.strptime(check_in_str, "%Y-%m-%d").date()
            req_out = datetime.datetime.strptime(check_out_str, "%Y-%m-%d").date()
        except Exception:
            return []

        for b in all_bookings:
            if b.get("status") in ["cancelled", "refunded"]:
                continue
            if exclude_booking_id and b.get("id") == exclude_booking_id:
                continue
            
            try:
                b_in = datetime.datetime.strptime(b.get("check_in"), "%Y-%m-%d").date()
                b_out = datetime.datetime.strptime(b.get("check_out"), "%Y-%m-%d").date()
            except Exception:
                continue
            
            # If not disjoint, they overlap
            if not (b_out <= req_in or b_in >= req_out):
                overlapping.append(b)

        return overlapping

    @staticmethod
    def update_status(booking_id: str, status: str) -> dict | None:
        if status not in ["pending", "confirmed", "cancelled", "completed"]:
            return None
        return db.update(COLLECTION, {"id": booking_id}, {"status": status})

    @staticmethod
    def delete(booking_id: str) -> bool:
        return db.delete(COLLECTION, {"id": booking_id})
