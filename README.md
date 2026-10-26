# 🏨 Hotel Room Booking System

> **A full-stack, enterprise-grade luxury hotel and room reservation system** engineered with a Python Flask RESTful micro-service backend, zero-collision calendar concurrency engine, PyJWT cryptographic authentication, and an ultra-modern Vanilla CSS luxury design system.

---

## 🌟 Key Features

- **Decoupled Architecture:** Clean separation of concerns across Routes, Models, Services, and Presentation.
- **Zero-Collision Date Overlap Guard:** Mathematical range checking prevents room double-booking under concurrent traffic.
- **Dynamic Pricing & Promo Engine:** Real-time calculation of night counts, base rates, 12% statutory luxury taxes, and promo code deductions (`LUXURY10`, `WELCOME50`, `SUMMER20`).
- **Cryptographic Authentication:** PBKDF2/scrypt password salting with HMAC-SHA256 JWT tokens (24-hour expiration) and Role-Based Access Control (`guest` vs `admin`).
- **Simulated Payment Gateway:** Multi-channel payment processing (Credit/Debit Card & UPI) generating traceable transaction IDs and instant folio emissions.
- **Printable Tax Invoices & Folios:** Automatic generation of formal electronic receipts with guest details, itemized tax breakdowns, and confirmation codes.
- **Zero-Configuration Local Execution:** Runs straight out-of-the-box with a built-in persistent datastore seeded with premier luxury hotels and resorts across Tamil Nadu (Chennai, Ooty, Kodaikanal, Madurai, and Mahabalipuram).

---

## 📁 Repository Structure

```
Hotel-Room-Booking-System/
│
├── documentation/
│   ├── Requirement_Analysis.docx      # Comprehensive feasibility & requirements study
│   └── SRS_Document.docx              # IEEE 830 compliant Software Requirements Specification
│
├── diagrams/
│   ├── Use_Case_Diagram.png           # UML Actor & functional boundary interactions
│   ├── Class_Diagram.png              # Entity models, relationships & multiplicities
│   ├── Sequence_Diagram.png           # Synchronous reservation & payment lifecycle flow
│   ├── Activity_Diagram.png           # Reservation decision branching & checkout workflow
│   ├── State_Chart_Diagram.png        # Booking status finite-state machine transitions
│   ├── Component_Diagram.png          # Subsystem decoupling, interfaces & data adapters
│   └── Deployment_Diagram.png         # Physical & distributed server/client topology
│
├── frontend/
│   ├── index.html                     # Luxury landing page & interactive search widget
│   ├── login.html                     # Member & Admin sign-in with quick-autofill buttons
│   ├── register.html                  # Member registration with validation
│   ├── hotels.html                    # Properties catalog with multi-attribute filters
│   ├── rooms.html                     # Suites & rooms view with real-time availability
│   ├── booking.html                   # Checkout flow, live billing calculator & payment modal
│   ├── my_bookings.html               # Guest itinerary dashboard, folios & cancellations
│   ├── css/
│   │   └── style.css                  # Bespoke luxury dark-mode design system
│   ├── js/
│   │   └── main.js                    # API client, JWT state manager & fallback store
│   └── images/                        # Showcase graphic assets
│
├── backend/
│   ├── app.py                         # Flask application factory, CORS & static serving
│   ├── config.py                      # Environment loader & configuration settings
│   ├── requirements.txt               # Backend Python dependencies
│   │
│   ├── routes/
│   │   ├── auth_routes.py             # User registration, login, profile & user listing
│   │   ├── hotel_routes.py            # Hotel query, filter & admin CRUD endpoints
│   │   ├── room_routes.py             # Suite search, availability checks & room management
│   │   ├── booking_routes.py          # Quote calculation, booking creation & lifecycle
│   │   └── payment_routes.py          # Transaction execution & receipt generation
│   │
│   ├── models/
│   │   ├── db_manager.py              # Thread-safe persistent storage engine
│   │   ├── user_model.py              # User schema & credential hashing logic
│   │   ├── hotel_model.py             # Hotel schema & search filters
│   │   ├── room_model.py              # Room schema & capacity rules
│   │   ├── booking_model.py           # Reservation schema & overlap query logic
│   │   └── payment_model.py           # Transaction settlement schema
│   │
│   ├── services/
│   │   ├── booking_service.py         # Date mathematics, promo discounts & tax logic
│   │   └── payment_service.py         # Mock gateway authorization & invoice generator
│   │
│   └── utils/
│       └── validators.py              # Email, phone, date validators & JWT decorators
│
├── database/
│   ├── collections_design.md          # Database schema specification, indexes & relations
│   └── sample_data.json               # Seed dataset for hotels, suites, users & bookings
│
├── testing/
│   ├── test_cases.docx                # Formal QA matrix with 25 passed test cases
│   └── postman_collection.json        # Postman v2.1 collection covering all 25 endpoints
│
├── screenshots/
│   ├── 01_Landing_Page.png            # Showcase screenshot: Home & Search
│   ├── 02_Hotels_Catalog.png          # Showcase screenshot: Properties Directory
│   ├── 03_Suites_Booking.png          # Showcase screenshot: Checkout & Billing
│   └── 04_Guest_Reservations.png      # Showcase screenshot: Guest Folio Dashboard
│
├── reports/
│   └── Final_Project_Report.docx      # 8-chapter engineering project report
│
├── .env                               # Environment configurations
├── .gitignore                         # Standard ignore rules for Python & web development
├── README.md                          # Comprehensive setup & API documentation
└── requirements.txt                   # Root Python dependencies
```

---

## ⚡ Quick Start & Execution

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Modern web browser (Chrome, Edge, Firefox, Safari)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Server

**Option A (Easiest — From Project Root):**
```bash
python run.py
```
*(Or double-click `start.bat` on Windows)*

**Option B (Standard):**
```bash
# If your terminal is in the project root:
python backend/app.py

# If your terminal is inside the backend directory:
python app.py
```

Visit the application in your browser:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

*Note: The Flask application automatically serves both the backend REST API (`/api/*`) and the frontend web pages (`/index.html`, `/hotels.html`, etc.) on port 5000! Detailed steps are in [STARTUP_GUIDE.md](file:///e:/HOTEL%20ROOM%20BOOKING%20SYSTEM/STARTUP_GUIDE.md).*

---

## 🔑 Demo Credentials

For instant evaluation, you can use the built-in one-click autofill buttons on the [Sign In page](http://127.0.0.1:5000/login.html) or enter:

| Role | Email | Password | Access Level |
|---|---|---|---|
| **Guest Member** | `sophia@example.com` | `password123` | Search, Book, View My Reservations, Print Invoices |
| **Administrator** | `admin@grandazure.com` | `admin123` | Full access, Hotel/Room Inventory CRUD, All Bookings |

---

## 🛡️ Concurrency & Date Overlap Prevention

To prevent double-booking when multiple guests reserve the same room simultaneously, the booking service evaluates:

$$\text{Collision} \iff \neg(\text{existing\_checkout} \le \text{new\_checkin} \lor \text{existing\_checkin} \ge \text{new\_checkout})$$

If any existing confirmed or pending reservation overlaps with the requested interval, the system immediately returns:
```json
{
  "success": false,
  "message": "Room is already reserved for the selected dates."
}
```

---

## 🏷️ Promotional Codes

During checkout, guests can enter coupon codes to receive discounts:
- **`LUXURY10`**: 10% discount on accommodation subtotal.
- **`WELCOME50`**: $50 flat discount on reservations of 2 or more nights.
- **`SUMMER20`**: 20% discount on stays of 3 or more nights.

---

## 🧪 Testing with Postman

1. Open Postman.
2. Click **Import** and select `testing/postman_collection.json`.
3. The collection is pre-configured with the `{{baseUrl}}` variable (`http://127.0.0.1:5000/api`).
4. Run the **Login Guest** request: it automatically extracts and stores the returned JWT token into `{{authToken}}` for all subsequent protected requests!

---

## 📄 Formal Documentation & Project Reports

| File | Format | Description |
|---|---|---|
| [Requirement_Analysis.docx](file:///e:/HOTEL%20ROOM%20BOOKING%20SYSTEM/documentation/Requirement_Analysis.docx) | Word .docx | Feasibility analysis, stakeholder personas, and operational requirements |
| [SRS_Document.docx](file:///e:/HOTEL%20ROOM%20BOOKING%20SYSTEM/documentation/SRS_Document.docx) | Word .docx | IEEE 830 standard software requirements specification |
| [test_cases.docx](file:///e:/HOTEL%20ROOM%20BOOKING%20SYSTEM/testing/test_cases.docx) | Word .docx | Detailed 25-case quality assurance matrix with 100% pass status |
| [Final_Project_Report.docx](file:///e:/HOTEL%20ROOM%20BOOKING%20SYSTEM/reports/Final_Project_Report.docx) | Word .docx | Academic and industrial final engineering project capstone report |

---

## 📐 UML Diagrams

High-resolution UML diagrams are located in the `diagrams/` folder:
- `Use_Case_Diagram.png`: Actor interactions, functional boundaries, and use cases.
- `Class_Diagram.png`: Domain entity classes, attributes, methods, and associations.
- `Sequence_Diagram.png`: Synchronous message flows across Guest, Frontend, API Services, Database, and Payment Gateway.
- `Activity_Diagram.png`: Reservation decision branching, date validation gates, and payment authorization.
- `State_Chart_Diagram.png`: Finite-state machine transitions across the booking lifecycle.
- `Component_Diagram.png`: Subsystem modularity, interfaces, and persistence repository adapters.
- `Deployment_Diagram.png`: Physical distributed client devices, application server runtime, and security perimeters.

---

## ⚖️ License & Credits

Developed for the **Hotel Room Booking System Platform**. All rights reserved &copy; 2026.
