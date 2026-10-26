import datetime
from backend.models.db_manager import db
from backend.utils.validators import generate_id, generate_transaction_id

COLLECTION = "payments"

class PaymentModel:
    @staticmethod
    def create(data: dict) -> dict:
        payment_id = generate_id("pay")
        transaction_id = data.get("transaction_id") or generate_transaction_id()
        now = datetime.datetime.utcnow().isoformat() + "Z"
        
        payment_doc = {
            "id": payment_id,
            "booking_id": data.get("booking_id"),
            "user_id": data.get("user_id"),
            "transaction_id": transaction_id,
            "amount": float(data.get("amount", 0.0)),
            "currency": data.get("currency", "USD"),
            "payment_method": data.get("payment_method", "credit_card"),
            "payment_status": data.get("payment_status", "completed"),
            "payment_date": now
        }
        
        db.insert(COLLECTION, payment_doc)
        return payment_doc

    @staticmethod
    def find_by_booking(booking_id: str) -> list[dict]:
        return db.find(COLLECTION, {"booking_id": booking_id})

    @staticmethod
    def find_by_id(payment_id: str) -> dict | None:
        return db.find_one(COLLECTION, {"id": payment_id})

    @staticmethod
    def find_by_transaction_id(transaction_id: str) -> dict | None:
        return db.find_one(COLLECTION, {"transaction_id": transaction_id})

    @staticmethod
    def update_status(payment_id: str, status: str) -> dict | None:
        if status not in ["pending", "completed", "failed", "refunded"]:
            return None
        return db.update(COLLECTION, {"id": payment_id}, {"payment_status": status})

    @staticmethod
    def delete_by_booking(booking_id: str) -> bool:
        return db.delete(COLLECTION, {"booking_id": booking_id})
