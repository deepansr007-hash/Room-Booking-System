import datetime
from backend.models.db_manager import db
from backend.utils.validators import generate_id

COLLECTION = "hotels"

class HotelModel:
    @staticmethod
    def create(data: dict) -> dict:
        hotel_id = generate_id("htl")
        now = datetime.datetime.utcnow().isoformat() + "Z"
        
        hotel_doc = {
            "id": hotel_id,
            "name": data.get("name", "").strip(),
            "description": data.get("description", "").strip(),
            "city": data.get("city", "").strip(),
            "state": data.get("state", "").strip(),
            "country": data.get("country", "").strip(),
            "address": data.get("address", "").strip(),
            "star_rating": float(data.get("star_rating", 4.5)),
            "images": data.get("images", []),
            "amenities": data.get("amenities", []),
            "contact_email": data.get("contact_email", "").strip(),
            "contact_phone": data.get("contact_phone", "").strip(),
            "created_at": now
        }
        
        db.insert(COLLECTION, hotel_doc)
        return hotel_doc

    @staticmethod
    def find_all(city: str = None, min_rating: float = None, query: str = None) -> list[dict]:
        hotels = db.get_all(COLLECTION)
        result = []
        
        for h in hotels:
            if city and city.lower() != "all" and city.lower() not in h.get("city", "").lower():
                continue
            if min_rating and h.get("star_rating", 0) < min_rating:
                continue
            if query:
                q = query.lower()
                text_match = (
                    q in h.get("name", "").lower()
                    or q in h.get("city", "").lower()
                    or q in h.get("description", "").lower()
                    or any(q in a.lower() for a in h.get("amenities", []))
                )
                if not text_match:
                    continue
            result.append(h)
        return result

    @staticmethod
    def find_by_id(hotel_id: str) -> dict | None:
        return db.find_one(COLLECTION, {"id": hotel_id})

    @staticmethod
    def update(hotel_id: str, data: dict) -> dict | None:
        allowed = {
            "name", "description", "city", "state", "country", "address",
            "star_rating", "images", "amenities", "contact_email", "contact_phone"
        }
        filtered = {k: v for k, v in data.items() if k in allowed}
        return db.update(COLLECTION, {"id": hotel_id}, filtered)

    @staticmethod
    def delete(hotel_id: str) -> bool:
        return db.delete(COLLECTION, {"id": hotel_id})
