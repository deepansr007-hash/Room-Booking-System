# Database & Collections Architecture Design
## Hotel Room Booking System

This document outlines the database architecture, schema definitions, indexes, entity relationships, and integrity rules for the Hotel Room Booking System. The system is designed to support both MongoDB (document-oriented) and Relational/SQLite environments seamlessly.

---

## 1. Entity Relationship Overview

```
 [User] 1 ────< (manages/owns)
   │
   │ 1
   │
   └──< [Booking] >──── 1 [Room] >──── 1 [Hotel]
            │
            │ 1
            │
            v 1
        [Payment]
```

---

## 2. Collections / Tables Specifications

### 2.1 `users` Collection
Stores registered guests and administrative personnel credentials, profile data, and roles.

| Field Name | Type | Constraints | Description |
|---|---|---|---|
| `_id` / `id` | String / UUID | Primary Key | Unique user identifier |
| `name` | String | Required, Min 2 chars | Full name of the user |
| `email` | String | Required, Unique, Indexed | Valid email address for authentication |
| `password_hash` | String | Required | Werkzeug pbkdf2:sha256 hash |
| `phone` | String | Required, 10-15 digits | Contact phone number |
| `role` | String | Enum: `['guest', 'admin']` | Authorization role (default: `guest`) |
| `created_at` | DateTime / ISO8601 | Default: UTC now | Account creation timestamp |
| `updated_at` | DateTime / ISO8601 | Default: UTC now | Profile last update timestamp |

**Indexes:**
- `{ "email": 1 }` (Unique)
- `{ "role": 1 }`

---

### 2.2 `hotels` Collection
Stores properties, locations, amenities, star ratings, and contact info.

| Field Name | Type | Constraints | Description |
|---|---|---|---|
| `_id` / `id` | String / UUID | Primary Key | Unique hotel identifier |
| `name` | String | Required, Indexed | Hotel commercial name |
| `description` | String | Required | Rich narrative of property |
| `city` | String | Required, Indexed | City location |
| `state` | String | Required | State or province |
| `country` | String | Required | Country name |
| `address` | String | Required | Street level address |
| `star_rating` | Float | Min 1.0, Max 5.0 | Official star category rating |
| `images` | Array[String] | Min 1 URL | Showcase and gallery image URLs |
| `amenities` | Array[String] | Array of tags | e.g., `["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Valet Parking"]` |
| `contact_email` | String | Email format | Hotel concierge/booking email |
| `contact_phone` | String | Phone format | Direct desk telephone |
| `created_at` | DateTime / ISO8601 | Default: UTC now | Creation timestamp |

**Indexes:**
- `{ "city": 1 }`
- `{ "star_rating": -1 }`
- `{ "name": "text", "city": "text", "description": "text" }` (Full-text search)

---

### 2.3 `rooms` Collection
Contains room units belonging to specific hotels, including tier, pricing, beds, capacity, and current availability status.

| Field Name | Type | Constraints | Description |
|---|---|---|---|
| `_id` / `id` | String / UUID | Primary Key | Unique room identifier |
| `hotel_id` | String / UUID | Foreign Key -> `hotels.id`, Indexed | Associated hotel |
| `room_number` | String | Required | Room door / room identifier (e.g., '101', 'Penthouse A') |
| `room_type` | String | Enum: `['Deluxe', 'Executive Suite', 'Presidential', 'Standard Single', 'Family Room']` | Category of room |
| `price_per_night` | Float | Min 1.00 | Rate per night in USD / INR |
| `capacity` | Integer | Min 1, Max 10 | Maximum adult guests |
| `bed_type` | String | e.g. `King Bed`, `Queen Double` | Bed configuration |
| `images` | Array[String] | Array of image URLs | Room interior photos |
| `features` | Array[String] | Array of tags | e.g., `["Ocean View", "Balcony", "Jacuzzi", "Mini Bar", "AC", "Smart TV"]` |
| `is_available` | Boolean | Default: True | General maintenance / active status |
| `created_at` | DateTime / ISO8601 | Default: UTC now | Timestamp |

**Indexes:**
- `{ "hotel_id": 1 }`
- `{ "room_type": 1 }`
- `{ "price_per_night": 1 }`
- `{ "hotel_id": 1, "is_available": 1 }`

---

### 2.4 `bookings` Collection
Handles reservations with reservation timeframes, guest details, price calculations, and lifecycle statuses.

| Field Name | Type | Constraints | Description |
|---|---|---|---|
| `_id` / `id` | String / UUID | Primary Key | Unique booking reservation reference |
| `booking_code` | String | Unique, Indexed | Human-readable reservation code (e.g. `BK-893421`) |
| `user_id` | String / UUID | Foreign Key -> `users.id`, Indexed | Booking guest reference |
| `hotel_id` | String / UUID | Foreign Key -> `hotels.id`, Indexed | Hotel reference |
| `room_id` | String / UUID | Foreign Key -> `rooms.id`, Indexed | Reserved room reference |
| `check_in` | Date (YYYY-MM-DD) | Required | Check-in date |
| `check_out` | Date (YYYY-MM-DD) | Required, > `check_in` | Check-out date |
| `num_guests` | Integer | Min 1 | Number of guests staying |
| `total_nights` | Integer | Min 1 | Calculated total nights |
| `price_per_night` | Float | Snapshot at booking time | Lock-in base price |
| `tax_amount` | Float | e.g. 12% GST/VAT | Calculated taxes |
| `discount_amount`| Float | Promo discounts applied | Deductions |
| `total_amount` | Float | Final net billable total | Payable price |
| `special_requests`| String | Optional | e.g. 'Late check-in', 'High floor' |
| `status` | String | Enum: `['pending', 'confirmed', 'cancelled', 'completed']` | Reservation lifecycle status |
| `created_at` | DateTime / ISO8601 | Default: UTC now | Reservation creation time |

**Indexes:**
- `{ "user_id": 1 }`
- `{ "room_id": 1, "check_in": 1, "check_out": 1, "status": 1 }` (Double-booking overlap check index)
- `{ "booking_code": 1 }` (Unique)

---

### 2.5 `payments` Collection
Maintains transactional records, gateway references, payment method, and settlement verification.

| Field Name | Type | Constraints | Description |
|---|---|---|---|
| `_id` / `id` | String / UUID | Primary Key | Unique payment record ID |
| `booking_id` | String / UUID | Foreign Key -> `bookings.id`, Indexed | Associated reservation |
| `user_id` | String / UUID | Foreign Key -> `users.id` | Paying user reference |
| `transaction_id` | String | Unique, Indexed | Simulated or real Gateway reference (e.g., `TXN_98726351`) |
| `amount` | Float | Required, Equals booking total | Amount paid |
| `currency` | String | Default: `USD` | ISO currency code |
| `payment_method` | String | Enum: `['credit_card', 'debit_card', 'upi', 'net_banking', 'paypal']` | Channel used |
| `payment_status` | String | Enum: `['pending', 'completed', 'failed', 'refunded']` | Transaction outcome |
| `receipt_url` | String | Optional | Link or generator key for receipt |
| `payment_date` | DateTime / ISO8601 | Default: UTC now | Transaction completion timestamp |

---

## 3. Data Integrity & Concurrency Control

1. **Overlap Prevention**: Before inserting any booking with status `confirmed` or `pending`, the service checks:
   ```sql
   SELECT COUNT(*) FROM bookings
   WHERE room_id = :room_id
     AND status IN ('confirmed', 'pending')
     AND NOT (check_out <= :new_check_in OR check_in >= :new_check_out);
   ```
   If count > 0, an `HTTP 409 Conflict: Room unavailable for selected dates` is returned.
2. **Transaction Atomicity**: In payment processing, the booking status transitions to `confirmed` only upon successful payment authorization.
3. **Cancellation Policy**: When a booking is cancelled, status updates to `cancelled`, and a refund record is generated in payments.
