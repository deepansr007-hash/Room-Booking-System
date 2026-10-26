import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models.db_manager import db
from backend.utils.validators import generate_id

COLLECTION = "users"

class UserModel:
    @staticmethod
    def create(name: str, email: str, password: str, phone: str, role: str = "guest") -> dict:
        user_id = generate_id("usr")
        now = datetime.datetime.utcnow().isoformat() + "Z"
        
        user_doc = {
            "id": user_id,
            "name": name.strip(),
            "email": email.strip().lower(),
            "password_hash": generate_password_hash(password),
            "phone": phone.strip(),
            "role": role if role in ["guest", "admin"] else "guest",
            "created_at": now,
            "updated_at": now
        }
        
        db.insert(COLLECTION, user_doc)
        return UserModel.to_dict(user_doc)

    @staticmethod
    def find_by_email(email: str) -> dict | None:
        if not email:
            return None
        return db.find_one(COLLECTION, {"email": email.strip().lower()})

    @staticmethod
    def find_by_id(user_id: str) -> dict | None:
        return db.find_one(COLLECTION, {"id": user_id})

    @staticmethod
    def get_all() -> list[dict]:
        users = db.get_all(COLLECTION)
        return [UserModel.to_dict(u) for u in users]

    @staticmethod
    def verify_password(stored_hash: str, password: str) -> bool:
        if not stored_hash or not password:
            return False
        return check_password_hash(stored_hash, password)

    @staticmethod
    def update_profile(user_id: str, fields: dict) -> dict | None:
        allowed = {"name", "phone"}
        filtered = {k: v for k, v in fields.items() if k in allowed}
        filtered["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
        updated = db.update(COLLECTION, {"id": user_id}, filtered)
        if updated:
            return UserModel.to_dict(updated)
        return None

    @staticmethod
    def update_role(user_id: str, new_role: str) -> dict | None:
        if new_role not in ["guest", "admin"]:
            return None
        updated = db.update(COLLECTION, {"id": user_id}, {
            "role": new_role,
            "updated_at": datetime.datetime.utcnow().isoformat() + "Z"
        })
        if updated:
            return UserModel.to_dict(updated)
        return None

    @staticmethod
    def delete(user_id: str) -> bool:
        return db.delete(COLLECTION, {"id": user_id})

    @staticmethod
    def to_dict(user: dict, include_hash: bool = False) -> dict:
        if not user:
            return {}
        data = dict(user)
        if not include_hash:
            data.pop("password_hash", None)
        return data
