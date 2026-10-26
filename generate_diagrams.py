import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DIAGRAMS_DIR = Path("e:/HOTEL ROOM BOOKING SYSTEM/diagrams")
DIAGRAMS_DIR.mkdir(parents=True, exist_ok=True)

# Colors
BG_COLOR = (15, 23, 42)        # Slate 900
BOX_BG = (30, 41, 59)          # Slate 800
BOX_BORDER = (212, 175, 55)    # Gold
TEXT_COLOR = (248, 250, 252)   # Off white
TEXT_MUTED = (148, 163, 184)   # Slate 400
TEXT_GOLD = (245, 230, 164)    # Pale gold
LINE_COLOR = (100, 116, 139)   # Slate 500
ACCENT_BLUE = (59, 130, 246)   # Blue
ACCENT_GREEN = (16, 185, 129)  # Green

def get_font(size):
    try:
        # Standard Windows fonts
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()

def draw_header(draw, title, subtitle):
    font_title = get_font(28)
    font_sub = get_font(15)
    draw.text((40, 30), title, fill=BOX_BORDER, font=font_title)
    draw.text((40, 68), subtitle, fill=TEXT_MUTED, font=font_sub)
    draw.line([(40, 95), (1360, 95)], fill=(51, 65, 85), width=2)

def draw_use_case():
    img = Image.new("RGB", (1400, 900), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "USE CASE DIAGRAM: HOTEL ROOM BOOKING SYSTEM", "Actor interactions, functional boundaries, and reservation lifecycle")
    
    font_box = get_font(14)
    font_actor = get_font(16)
    font_lbl = get_font(12)

    # System boundary box
    draw.rectangle([(320, 120), (1080, 840)], outline=BOX_BORDER, fill=(19, 29, 49), width=2)
    draw.text((340, 135), "System Boundary: Hotel Room Booking Core", fill=TEXT_GOLD, font=font_actor)

    # Actors
    # Guest
    draw.rectangle([(60, 320), (240, 480)], outline=ACCENT_BLUE, fill=BOX_BG, width=2)
    draw.ellipse([(125, 340), (175, 390)], outline=BOX_BORDER, fill=(37, 99, 235), width=2)
    draw.line([(150, 390), (150, 435)], fill=TEXT_COLOR, width=3)
    draw.line([(120, 405), (180, 405)], fill=TEXT_COLOR, width=3)
    draw.line([(150, 435), (130, 465)], fill=TEXT_COLOR, width=3)
    draw.line([(150, 435), (170, 465)], fill=TEXT_COLOR, width=3)
    draw.text((95, 495), "Guest / Member", fill=TEXT_COLOR, font=font_actor)

    # Admin
    draw.rectangle([(60, 600), (240, 760)], outline=ACCENT_BLUE, fill=BOX_BG, width=2)
    draw.ellipse([(125, 620), (175, 670)], outline=BOX_BORDER, fill=(217, 119, 6), width=2)
    draw.line([(150, 670), (150, 715)], fill=TEXT_COLOR, width=3)
    draw.line([(120, 685), (180, 685)], fill=TEXT_COLOR, width=3)
    draw.line([(150, 715), (130, 745)], fill=TEXT_COLOR, width=3)
    draw.line([(150, 715), (170, 745)], fill=TEXT_COLOR, width=3)
    draw.text((80, 775), "Hotel Operations Admin", fill=TEXT_COLOR, font=font_actor)

    # Payment Gateway
    draw.rectangle([(1160, 450), (1340, 560)], outline=(16, 185, 129), fill=BOX_BG, width=2)
    draw.text((1180, 475), "<<Service>>", fill=TEXT_MUTED, font=font_lbl)
    draw.text((1175, 500), "Payment Gateway", fill=TEXT_COLOR, font=font_actor)
    draw.text((1185, 525), "Secure API", fill=ACCENT_GREEN, font=font_lbl)

    # Use Cases (Ovals)
    cases = [
        ("Register & Authenticate Account", 400, 180),
        ("Browse Properties & Filter Rooms", 720, 180),
        ("Check Real-Time Availability", 400, 290),
        ("Calculate Pricing & Promo Discount", 720, 290),
        ("Initiate Room Reservation", 400, 410),
        ("Authorize Online Payment", 720, 410),
        ("Retrieve Electronic Tax Folio", 400, 530),
        ("Cancel Reservation & Request Refund", 720, 530),
        ("Manage Hotel & Room Inventories", 400, 650),
        ("Inspect Financial Reports & Audits", 720, 650),
        ("Configure System Parameters", 560, 760)
    ]

    for title, x, y in cases:
        draw.rounded_rectangle([(x, y), (x + 280, y + 65)], radius=30, outline=BOX_BORDER, fill=BOX_BG, width=2)
        draw.text((x + 20, y + 22), title, fill=TEXT_COLOR, font=font_box)

    # Connectors
    # Guest links
    guest_lines = [(240, 400, 400, 212), (240, 400, 720, 212), (240, 400, 400, 322),
                   (240, 400, 400, 442), (240, 400, 400, 562), (240, 400, 720, 562)]
    for x1, y1, x2, y2 in guest_lines:
        draw.line([(x1, y1), (x2, y2)], fill=LINE_COLOR, width=2)

    # Admin links
    admin_lines = [(240, 680, 400, 212), (240, 680, 400, 682), (240, 680, 720, 682), (240, 680, 560, 792)]
    for x1, y1, x2, y2 in admin_lines:
        draw.line([(x1, y1), (x2, y2)], fill=LINE_COLOR, width=2)

    # Payment Gateway links
    draw.line([(1000, 442), (1160, 505)], fill=ACCENT_GREEN, width=2)

    img.save(DIAGRAMS_DIR / "Use_Case_Diagram.png")
    print("Saved Use_Case_Diagram.png")

def draw_class_diagram():
    img = Image.new("RGB", (1400, 920), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "CLASS DIAGRAM: DOMAIN & PERSISTENCE ARCHITECTURE", "UML structural representation showing entity classes, attributes, methods, and associations")
    
    font_title = get_font(15)
    font_content = get_font(11)

    classes = [
        {"name": "User", "x": 60, "y": 140, "w": 260, "h": 220,
         "attrs": ["+ id: String [PK]", "+ name: String", "+ email: String [Unique]", "+ password_hash: String", "+ phone: String", "+ role: Enum(guest, admin)"],
         "methods": ["+ create(): User", "+ verify_password(): Bool", "+ update_profile(): User"]},
        
        {"name": "Hotel", "x": 420, "y": 140, "w": 280, "h": 240,
         "attrs": ["+ id: String [PK]", "+ name: String", "+ city: String", "+ address: String", "+ star_rating: Float", "+ amenities: List[String]"],
         "methods": ["+ find_all(filters): List", "+ find_by_id(id): Hotel", "+ create(data): Hotel", "+ update(id, data): Hotel"]},

        {"name": "Room", "x": 800, "y": 140, "w": 280, "h": 240,
         "attrs": ["+ id: String [PK]", "+ hotel_id: String [FK]", "+ room_number: String", "+ room_type: String", "+ price_per_night: Float", "+ capacity: Int", "+ is_available: Bool"],
         "methods": ["+ find_by_hotel(): List", "+ check_availability(): Bool", "+ update_status(): Room"]},

        {"name": "Booking", "x": 240, "y": 480, "w": 320, "h": 320,
         "attrs": ["+ id: String [PK]", "+ booking_code: String", "+ user_id: String [FK]", "+ hotel_id: String [FK]", "+ room_id: String [FK]", "+ check_in: Date", "+ check_out: Date", "+ total_nights: Int", "+ total_amount: Float", "+ status: Enum"],
         "methods": ["+ create(data): Booking", "+ find_by_user(): List", "+ find_overlapping(): List", "+ cancel(): Booking", "+ update_status(): Booking"]},

        {"name": "Payment", "x": 720, "y": 480, "w": 300, "h": 280,
         "attrs": ["+ id: String [PK]", "+ booking_id: String [FK]", "+ user_id: String [FK]", "+ transaction_id: String", "+ amount: Float", "+ currency: String", "+ payment_method: String", "+ payment_status: Enum"],
         "methods": ["+ create(data): Payment", "+ find_by_booking(): List", "+ generate_receipt(): Dict"]},

        {"name": "BookingService", "x": 1090, "y": 280, "w": 280, "h": 220,
         "attrs": ["- tax_rate: Float = 0.12", "- promo_rules: Dict"],
         "methods": ["+ calculate_price(): Dict", "+ check_availability(): Dict", "+ create_reservation(): Booking", "+ cancel_reservation(): Booking"]}
    ]

    for c in classes:
        x, y, w, h = c["x"], c["y"], c["w"], c["h"]
        draw.rectangle([(x, y), (x + w, y + h)], outline=BOX_BORDER, fill=BOX_BG, width=2)
        # Title bar
        draw.rectangle([(x, y), (x + w, y + 36)], fill=(51, 65, 85))
        draw.text((x + 15, y + 10), c["name"], fill=TEXT_GOLD, font=font_title)
        
        # Attributes divider
        curr_y = y + 46
        for attr in c["attrs"]:
            draw.text((x + 12, curr_y), attr, fill=TEXT_COLOR, font=font_content)
            curr_y += 18
        
        draw.line([(x, curr_y + 4), (x + w, curr_y + 4)], fill=LINE_COLOR, width=1)
        curr_y += 12
        for m in c["methods"]:
            draw.text((x + 12, curr_y), m, fill=TEXT_MUTED, font=font_content)
            curr_y += 18

    # Multiplicity & Connectors
    # User to Booking (1 to 0..*)
    draw.line([(190, 360), (190, 600), (240, 600)], fill=LINE_COLOR, width=2)
    draw.text((200, 370), "1", fill=TEXT_GOLD, font=font_content)
    draw.text((205, 580), "0..*", fill=TEXT_GOLD, font=font_content)

    # Hotel to Room (1 to 1..*)
    draw.line([(700, 260), (800, 260)], fill=LINE_COLOR, width=2)
    draw.text((710, 240), "1", fill=TEXT_GOLD, font=font_content)
    draw.text((780, 240), "1..*", fill=TEXT_GOLD, font=font_content)

    # Room to Booking (1 to 0..*)
    draw.line([(940, 380), (940, 440), (500, 440), (500, 480)], fill=LINE_COLOR, width=2)
    draw.text((945, 390), "1", fill=TEXT_GOLD, font=font_content)
    draw.text((505, 455), "0..*", fill=TEXT_GOLD, font=font_content)

    # Booking to Payment (1 to 1)
    draw.line([(560, 620), (720, 620)], fill=LINE_COLOR, width=2)
    draw.text((570, 600), "1", fill=TEXT_GOLD, font=font_content)
    draw.text((700, 600), "1", fill=TEXT_GOLD, font=font_content)

    img.save(DIAGRAMS_DIR / "Class_Diagram.png")
    print("Saved Class_Diagram.png")

def draw_sequence_diagram():
    img = Image.new("RGB", (1400, 900), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "SEQUENCE DIAGRAM: ROOM RESERVATION & PAYMENT EXECUTION", "Synchronous message flows across Guest, Frontend, API Services, Database, and Payment Gateway")
    
    font_box = get_font(13)
    font_msg = get_font(11)

    actors = [
        ("Guest Client", 100),
        ("Frontend WebApp", 340),
        ("BookingService", 580),
        ("PaymentGateway", 860),
        ("Database / Model", 1140)
    ]

    for name, x in actors:
        draw.rectangle([(x - 80, 130), (x + 80, 175)], outline=BOX_BORDER, fill=BOX_BG, width=2)
        draw.text((x - 65, 145), name, fill=TEXT_GOLD, font=font_box)
        draw.line([(x, 175), (x, 840)], fill=(71, 85, 105), width=2)

    messages = [
        (100, 340, 210, "1: Select Room, Dates & Guests", True),
        (340, 580, 250, "2: POST /api/bookings/quote", True),
        (580, 1140, 290, "3: Check overlapping bookings", True),
        (1140, 580, 330, "4: Return availability & pricing data", False),
        (580, 340, 370, "5: 200 OK (Calculated total, taxes, discounts)", False),
        (340, 100, 410, "6: Display Bill Summary & Payment Form", False),
        (100, 340, 460, "7: Submit Payment (Card / UPI details)", True),
        (340, 580, 500, "8: POST /api/bookings (Create Pending)", True),
        (580, 1140, 540, "9: INSERT INTO bookings (status: 'pending')", True),
        (580, 860, 590, "10: Process Payment Transaction ($Amount)", True),
        (860, 580, 640, "11: 200 Authorized (TXN_98726351)", False),
        (580, 1140, 690, "12: UPDATE bookings SET status='confirmed'", True),
        (580, 1140, 730, "13: INSERT INTO payments (status: 'completed')", True),
        (580, 340, 770, "14: 200 OK (Booking confirmed, Folio emitted)", False),
        (340, 100, 810, "15: Display Confirmation Modal & Digital Receipt", False)
    ]

    for x1, x2, y, text, is_sync in messages:
        color = ACCENT_BLUE if is_sync else ACCENT_GREEN
        draw.line([(x1, y), (x2, y)], fill=color, width=2)
        # Arrowhead
        if x2 > x1:
            draw.polygon([(x2, y), (x2 - 10, y - 5), (x2 - 10, y + 5)], fill=color)
        else:
            draw.polygon([(x2, y), (x2 + 10, y - 5), (x2 + 10, y + 5)], fill=color)
        
        mid_x = (x1 + x2) // 2
        draw.text((mid_x - 120, y - 16), text, fill=TEXT_COLOR, font=font_msg)

    img.save(DIAGRAMS_DIR / "Sequence_Diagram.png")
    print("Saved Sequence_Diagram.png")

def draw_activity_diagram():
    img = Image.new("RGB", (1400, 920), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "ACTIVITY DIAGRAM: RESERVATION & CHECKOUT WORKFLOW", "Activity states, branch decisions, validation gates, and payment handling")

    font_box = get_font(13)
    font_lbl = get_font(11)

    # Initial State
    draw.ellipse([(680, 120), (720, 160)], fill=ACCENT_BLUE, outline=BOX_BORDER, width=2)
    draw.line([(700, 160), (700, 200)], fill=LINE_COLOR, width=2)

    steps = [
        ("Search Properties & Select Desired Suite", 200),
        ("Choose Check-in / Check-out Dates & Guests", 290)
    ]

    for title, y in steps:
        draw.rounded_rectangle([(520, y), (880, y + 50)], radius=15, outline=BOX_BORDER, fill=BOX_BG, width=2)
        draw.text((540, y + 16), title, fill=TEXT_COLOR, font=font_box)
        draw.line([(700, y + 50), (700, y + 90)], fill=LINE_COLOR, width=2)

    # Decision 1: Room Available?
    draw.polygon([(700, 380), (770, 425), (700, 470), (630, 425)], outline=BOX_BORDER, fill=(51, 65, 85), width=2)
    draw.text((655, 417), "Available?", fill=TEXT_GOLD, font=font_lbl)

    # Decision 1 No branch
    draw.line([(630, 425), (360, 425), (360, 225), (520, 225)], fill=(239, 68, 68), width=2)
    draw.text((420, 405), "[No: Dates Booked]", fill=(248, 113, 113), font=font_lbl)

    # Decision 1 Yes branch
    draw.line([(700, 470), (700, 520)], fill=ACCENT_GREEN, width=2)
    draw.text((710, 485), "[Yes]", fill=ACCENT_GREEN, font=font_lbl)

    # Next steps
    draw.rounded_rectangle([(520, 520), (880, 570)], radius=15, outline=BOX_BORDER, fill=BOX_BG, width=2)
    draw.text((550, 536), "Calculate Rate, Taxes & Apply Promo Code", fill=TEXT_COLOR, font=font_box)
    draw.line([(700, 570), (700, 610)], fill=LINE_COLOR, width=2)

    draw.rounded_rectangle([(520, 610), (880, 660)], radius=15, outline=BOX_BORDER, fill=BOX_BG, width=2)
    draw.text((550, 626), "Submit Payment Method (Card / UPI)", fill=TEXT_COLOR, font=font_box)
    draw.line([(700, 660), (700, 700)], fill=LINE_COLOR, width=2)

    # Decision 2: Payment Authorized?
    draw.polygon([(700, 700), (770, 745), (700, 790), (630, 745)], outline=BOX_BORDER, fill=(51, 65, 85), width=2)
    draw.text((650, 737), "Authorized?", fill=TEXT_GOLD, font=font_lbl)

    # Decision 2 No branch
    draw.line([(770, 745), (1040, 745), (1040, 635), (880, 635)], fill=(239, 68, 68), width=2)
    draw.text((890, 725), "[Payment Failed: Re-enter]", fill=(248, 113, 113), font=font_lbl)

    # Decision 2 Yes branch
    draw.line([(700, 790), (700, 830)], fill=ACCENT_GREEN, width=2)
    draw.text((710, 805), "[Success]", fill=ACCENT_GREEN, font=font_lbl)

    draw.rounded_rectangle([(500, 830), (900, 880)], radius=15, outline=BOX_BORDER, fill=BOX_BG, width=2)
    draw.text((530, 846), "Confirm Booking, Generate Folio & Send Email", fill=TEXT_COLOR, font=font_box)

    # Final State Bullseye
    draw.ellipse([(940, 835), (980, 875)], outline=BOX_BORDER, fill=BOX_BG, width=2)
    draw.ellipse([(948, 843), (972, 867)], fill=ACCENT_GREEN)

    img.save(DIAGRAMS_DIR / "Activity_Diagram.png")
    print("Saved Activity_Diagram.png")

def draw_state_chart_diagram():
    img = Image.new("RGB", (1400, 850), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "STATE CHART DIAGRAM: RESERVATION LIFECYCLE", "State machine transitions from Draft initiation to Completion or Cancellation")

    font_box = get_font(14)
    font_lbl = get_font(12)

    states = [
        {"name": "DRAFT / BROWSING", "x": 100, "y": 360, "w": 220, "h": 90, "desc": "Room & dates chosen in UI"},
        {"name": "PENDING_PAYMENT", "x": 420, "y": 360, "w": 240, "h": 90, "desc": "Locked for checkout window"},
        {"name": "CONFIRMED", "x": 760, "y": 360, "w": 220, "h": 90, "desc": "Payment settled & verified"},
        {"name": "COMPLETED", "x": 1100, "y": 360, "w": 220, "h": 90, "desc": "Guest check-out finalized"},
        {"name": "CANCELLED", "x": 600, "y": 580, "w": 220, "h": 90, "desc": "Cancelled & refund processed"}
    ]

    # Initial state
    draw.ellipse([(30, 390), (60, 420)], fill=ACCENT_BLUE, outline=BOX_BORDER, width=2)
    draw.line([(60, 405), (100, 405)], fill=LINE_COLOR, width=2)

    for s in states:
        x, y, w, h = s["x"], s["y"], s["w"], s["h"]
        draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=15, outline=BOX_BORDER, fill=BOX_BG, width=2)
        draw.text((x + 20, y + 20), s["name"], fill=TEXT_GOLD, font=font_box)
        draw.text((x + 20, y + 50), s["desc"], fill=TEXT_MUTED, font=font_lbl)

    # Transitions
    # Draft -> Pending
    draw.line([(320, 405), (420, 405)], fill=LINE_COLOR, width=2)
    draw.text((330, 380), "Proceed", fill=TEXT_COLOR, font=font_lbl)

    # Pending -> Confirmed
    draw.line([(660, 405), (760, 405)], fill=ACCENT_GREEN, width=2)
    draw.text((670, 380), "Payment OK", fill=ACCENT_GREEN, font=font_lbl)

    # Confirmed -> Completed
    draw.line([(980, 405), (1100, 405)], fill=LINE_COLOR, width=2)
    draw.text((1000, 380), "Stay Complete", fill=TEXT_COLOR, font=font_lbl)

    # Pending -> Cancelled (Timeout)
    draw.line([(540, 450), (540, 520), (660, 520), (660, 580)], fill=(239, 68, 68), width=2)
    draw.text((480, 480), "Timeout / Drop", fill=(248, 113, 113), font=font_lbl)

    # Confirmed -> Cancelled (Guest/Admin cancel)
    draw.line([(870, 450), (870, 520), (760, 520), (760, 580)], fill=(239, 68, 68), width=2)
    draw.text((880, 480), "Cancel Reservation", fill=(248, 113, 113), font=font_lbl)

    # Final bullseyes
    # After completed
    draw.ellipse([(1340, 395), (1370, 425)], outline=BOX_BORDER, fill=BOX_BG, width=2)
    draw.ellipse([(1347, 402), (1363, 418)], fill=ACCENT_GREEN)
    draw.line([(1320, 410), (1340, 410)], fill=LINE_COLOR, width=2)

    # After cancelled
    draw.ellipse([(840, 615), (870, 645)], outline=BOX_BORDER, fill=BOX_BG, width=2)
    draw.ellipse([(847, 622), (863, 638)], fill=(239, 68, 68))
    draw.line([(820, 630), (840, 630)], fill=LINE_COLOR, width=2)

    img.save(DIAGRAMS_DIR / "State_Chart_Diagram.png")
    print("Saved State_Chart_Diagram.png")

def draw_component_diagram():
    img = Image.new("RGB", (1400, 900), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "COMPONENT DIAGRAM: SYSTEM SUBSYSTEMS & INTERFACES", "Component modularity, ports, interfaces, and decoupling boundaries")

    font_box = get_font(15)
    font_lbl = get_font(12)

    components = [
        {"name": "Client Presentation Layer", "sub": "HTML5, Vanilla CSS, JS Engine", "x": 80, "y": 200, "w": 340, "h": 140},
        {"name": "REST API Gateway & Routing", "sub": "Flask Application Factory & CORS", "x": 520, "y": 200, "w": 360, "h": 140},
        {"name": "Authentication & JWT Subsystem", "sub": "Token Signer, RBAC Guard", "x": 980, "y": 200, "w": 340, "h": 140},
        {"name": "Booking & Pricing Engine", "sub": "Collision Check, Tax, Promo Rules", "x": 240, "y": 480, "w": 380, "h": 150},
        {"name": "Payment Gateway Adapter", "sub": "Secure Sandbox / Provider Driver", "x": 760, "y": 480, "w": 380, "h": 150},
        {"name": "Persistence Repository Layer", "sub": "SQLite / JSON Active Datastore / Mongo", "x": 500, "y": 700, "w": 400, "h": 140}
    ]

    for c in components:
        x, y, w, h = c["x"], c["y"], c["w"], c["h"]
        draw.rectangle([(x, y), (x + w, y + h)], outline=BOX_BORDER, fill=BOX_BG, width=2)
        # UML component tabs
        draw.rectangle([(x - 12, y + 20), (x + 8, y + 45)], outline=BOX_BORDER, fill=(51, 65, 85), width=2)
        draw.rectangle([(x - 12, y + 60), (x + 8, y + 85)], outline=BOX_BORDER, fill=(51, 65, 85), width=2)
        
        draw.text((x + 25, y + 35), c["name"], fill=TEXT_GOLD, font=font_box)
        draw.text((x + 25, y + 75), c["sub"], fill=TEXT_MUTED, font=font_lbl)

    # Connections
    # Client to API
    draw.line([(420, 270), (520, 270)], fill=LINE_COLOR, width=3)
    draw.text((435, 245), "HTTP/JSON", fill=TEXT_COLOR, font=font_lbl)

    # API to Auth
    draw.line([(880, 270), (980, 270)], fill=LINE_COLOR, width=3)
    draw.text((895, 245), "Validate", fill=TEXT_COLOR, font=font_lbl)

    # API to Booking Engine
    draw.line([(650, 340), (430, 480)], fill=LINE_COLOR, width=3)

    # API to Payment Adapter
    draw.line([(750, 340), (950, 480)], fill=LINE_COLOR, width=3)

    # Booking Engine to Persistence
    draw.line([(430, 630), (600, 700)], fill=LINE_COLOR, width=3)

    # Payment Adapter to Persistence
    draw.line([(950, 630), (780, 700)], fill=LINE_COLOR, width=3)

    img.save(DIAGRAMS_DIR / "Component_Diagram.png")
    print("Saved Component_Diagram.png")

def draw_deployment_diagram():
    img = Image.new("RGB", (1400, 900), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "DEPLOYMENT DIAGRAM: DISTRIBUTED TOPOLOGY & HARDWARE NODES", "Physical / cloud host execution environments, protocols, and security perimeters")

    font_box = get_font(15)
    font_lbl = get_font(12)

    # Node 1: Client Tier
    draw.rectangle([(60, 240), (380, 660)], outline=BOX_BORDER, fill=BOX_BG, width=2)
    draw.rectangle([(60, 240), (380, 280)], fill=(51, 65, 85))
    draw.text((80, 252), "<<device>> Client Tier", fill=TEXT_GOLD, font=font_box)
    
    # Artifact inside Client
    draw.rectangle([(90, 320), (350, 440)], outline=LINE_COLOR, fill=(19, 29, 49), width=1)
    draw.text((110, 340), "<<artifact>> Web Browser", fill=TEXT_COLOR, font=font_box)
    draw.text((110, 375), "SPA Client (HTML5 / ES6)", fill=TEXT_MUTED, font=font_lbl)
    draw.text((110, 400), "Local JWT Token Storage", fill=TEXT_MUTED, font=font_lbl)

    # Node 2: Web / App Server Tier
    draw.rectangle([(480, 180), (920, 720)], outline=BOX_BORDER, fill=BOX_BG, width=2)
    draw.rectangle([(480, 180), (920, 220)], fill=(51, 65, 85))
    draw.text((500, 192), "<<execution environment>> Backend Host", fill=TEXT_GOLD, font=font_box)

    # Artifacts inside Backend
    draw.rectangle([(510, 260), (890, 420)], outline=LINE_COLOR, fill=(19, 29, 49), width=1)
    draw.text((530, 280), "<<process>> Python 3.13 Runtime", fill=TEXT_COLOR, font=font_box)
    draw.text((530, 320), "Flask Microframework (WSGI / Uvicorn)", fill=TEXT_MUTED, font=font_lbl)
    draw.text((530, 345), "PyJWT Cryptographic Engine", fill=TEXT_MUTED, font=font_lbl)
    draw.text((530, 370), "Service Controllers & Validators", fill=TEXT_MUTED, font=font_lbl)

    draw.rectangle([(510, 460), (890, 670)], outline=LINE_COLOR, fill=(19, 29, 49), width=1)
    draw.text((530, 480), "<<subsystem>> Database Node", fill=TEXT_COLOR, font=font_box)
    draw.text((530, 520), "SQLite Engine / Active JSON Store", fill=TEXT_MUTED, font=font_lbl)
    draw.text((530, 550), "ACID Transactions & Overlap Guard", fill=TEXT_MUTED, font=font_lbl)
    draw.text((530, 580), "Thread-Safe File / Disk Persistence", fill=TEXT_MUTED, font=font_lbl)

    # Node 3: External Payment Service
    draw.rectangle([(1020, 320), (1340, 540)], outline=ACCENT_GREEN, fill=BOX_BG, width=2)
    draw.rectangle([(1020, 320), (1340, 360)], fill=(6, 95, 70))
    draw.text((1040, 332), "<<cloud>> Payment Gateway", fill=TEXT_COLOR, font=font_box)
    draw.text((1040, 390), "PCI-DSS Compliant Endpoint", fill=TEXT_COLOR, font=font_lbl)
    draw.text((1040, 420), "Sandbox / Production API", fill=TEXT_MUTED, font=font_lbl)
    draw.text((1040, 450), "TLS 1.3 / AES-256", fill=ACCENT_GREEN, font=font_lbl)

    # Connectors
    # Client to Backend
    draw.line([(380, 380), (480, 380)], fill=LINE_COLOR, width=3)
    draw.text((395, 355), "HTTPS / REST", fill=TEXT_COLOR, font=font_lbl)

    # Backend to Payment
    draw.line([(890, 380), (1020, 380)], fill=ACCENT_GREEN, width=3)
    draw.text((915, 355), "mTLS API", fill=ACCENT_GREEN, font=font_lbl)

    img.save(DIAGRAMS_DIR / "Deployment_Diagram.png")
    print("Saved Deployment_Diagram.png")

if __name__ == "__main__":
    draw_use_case()
    draw_class_diagram()
    draw_sequence_diagram()
    draw_activity_diagram()
    draw_state_chart_diagram()
    draw_component_diagram()
    draw_deployment_diagram()
    print("All 7 UML diagrams successfully generated!")
