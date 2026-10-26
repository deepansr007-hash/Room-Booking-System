import datetime
from backend.models.db_manager import db
from backend.utils.validators import generate_id

COLLECTION = "rooms"

class RoomModel:
    @staticmethod
    def create(data: dict) -> dict:
        room_id = generate_id("rm")
        now = datetime.datetime.utcnow().isoformat() + "Z"
        
        room_doc = {
            "id": room_id,
            "hotel_id": data.get("hotel_id"),
            "room_number": data.get("room_number", "").strip(),
            "room_type": data.get("room_type", "Deluxe"),
            "price_per_night": float(data.get("price_per_night", 100.0)),
            "capacity": int(data.get("capacity", 2)),
            "bed_type": data.get("bed_type", "King Bed"),
            "images": data.get("images", []),
            "features": data.get("features", []),
            "is_available": data.get("is_available", True),
            "created_at": now
        }
        
        db.insert(COLLECTION, room_doc)
        return room_doc

    @staticmethod
    def find_by_hotel(hotel_id: str) -> list[dict]:
        return db.find(COLLECTION, {"hotel_id": hotel_id})

    @staticmethod
    def find_by_id(room_id: str) -> dict | None:
        return db.find_one(COLLECTION, {"id": room_id})

    @staticmethod
    def find_all(max_price: float = None, room_type: str = None, capacity: int = None) -> list[dict]:
        rooms = db.get_all(COLLECTION)
        result = []
        for r in rooms:
            if max_price and r.get("price_per_night", 0) > max_price:
                continue
            if room_type and room_type.lower() != "all" and room_type.lower() not in r.get("room_type", "").lower():
                continue
            if capacity and r.get("capacity", 0) < capacity:
                continue
            result.append(r)
        return result

    @staticmethod
    def update(room_id: str, data: dict) -> dict | None:
        allowed = {
            "room_number", "room_type", "price_per_night",
            "capacity", "bed_type", "images", "features", "is_available"
        }
        filtered = {k: v for k, v in data.items() if k in allowed}
        return db.update(COLLECTION, {"id": room_id}, filtered)

    @staticmethod
    def delete(room_id: str) -> bool:
        return db.delete(COLLECTION, {"id": room_id})
