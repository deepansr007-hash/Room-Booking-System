import datetime
from backend.models.booking_model import BookingModel
from backend.models.payment_model import PaymentModel
from backend.models.hotel_model import HotelModel
from backend.models.room_model import RoomModel
from backend.models.user_model import UserModel
from backend.utils.validators import generate_transaction_id

class PaymentService:
    @staticmethod
    def process_payment(booking_id: str, user_id: str, payment_method: str = "credit_card", details: dict = None) -> dict:
        booking = BookingModel.find_by_id(booking_id)
        if not booking:
            raise ValueError(f"Booking '{booking_id}' not found.")

        if booking.get("user_id") != user_id:
            raise PermissionError("Access denied: You do not own this reservation.")

        if booking.get("status") == "confirmed":
            existing_payments = PaymentModel.find_by_booking(booking_id)
            if existing_payments:
                return {
                    "success": True,
                    "message": "Booking is already paid and confirmed.",
                    "payment": existing_payments[0]
                }

        if booking.get("status") == "cancelled":
            raise ValueError("Cannot pay for a cancelled reservation.")

        # Payment details verification simulation
        if payment_method in ["credit_card", "debit_card"]:
            card_num = (details or {}).get("card_number", "").replace(" ", "").replace("-", "")
            if card_num and len(card_num) < 13:
                raise ValueError("Invalid card number format.")
        elif payment_method == "upi":
            upi_id = (details or {}).get("upi_id", "")
            if upi_id and "@" not in upi_id:
                raise ValueError("Invalid UPI ID format. Must contain '@'.")

        transaction_id = generate_transaction_id()
        amount = float(booking.get("total_amount", 0.0))

        payment_data = {
            "booking_id": booking_id,
            "user_id": user_id,
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": "USD",
            "payment_method": payment_method,
            "payment_status": "completed"
        }

        payment = PaymentModel.create(payment_data)

        # Update booking status to confirmed
        BookingModel.update_status(booking_id, "confirmed")

        return {
            "success": True,
            "message": "Payment authorized and booking confirmed successfully.",
            "payment": payment
        }

    @staticmethod
    def get_receipt(payment_id: str) -> dict:
        payment = PaymentModel.find_by_id(payment_id)
        if not payment:
            raise ValueError("Payment record not found.")

        booking = BookingModel.find_by_id(payment.get("booking_id"))
        hotel = HotelModel.find_by_id(booking.get("hotel_id")) if booking else None
        room = RoomModel.find_by_id(booking.get("room_id")) if booking else None
        user = UserModel.find_by_id(payment.get("user_id"))

        return {
            "receipt_number": f"REC-{payment.get('transaction_id')}",
            "transaction_id": payment.get("transaction_id"),
            "payment_date": payment.get("payment_date"),
            "payment_method": payment.get("payment_method"),
            "payment_status": payment.get("payment_status"),
            "currency": payment.get("currency", "USD"),
            "amount_paid": payment.get("amount"),
            "guest": {
                "name": user.get("name") if user else "Valued Guest",
                "email": user.get("email") if user else "N/A",
                "phone": user.get("phone") if user else "N/A"
            },
            "reservation": {
                "booking_code": booking.get("booking_code") if booking else "N/A",
                "hotel_name": hotel.get("name") if hotel else "Luxury Hotel",
                "hotel_address": hotel.get("address") if hotel else "",
                "room_type": room.get("room_type") if room else "Standard Room",
                "room_number": room.get("room_number") if room else "",
                "check_in": booking.get("check_in") if booking else "",
                "check_out": booking.get("check_out") if booking else "",
                "total_nights": booking.get("total_nights") if booking else 1,
                "price_per_night": booking.get("price_per_night") if booking else 0.0,
                "tax_amount": booking.get("tax_amount") if booking else 0.0,
                "discount_amount": booking.get("discount_amount") if booking else 0.0,
                "total_amount": booking.get("total_amount") if booking else 0.0
            }
        }
