import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SCREENSHOTS_DIR = Path("e:/HOTEL ROOM BOOKING SYSTEM/screenshots")
IMAGES_DIR = Path("e:/HOTEL ROOM BOOKING SYSTEM/frontend/images")

SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def create_preview_card(path, title, subtitle, tag, color_accent):
    img = Image.new("RGB", (1280, 800), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    # Outer luxury border
    draw.rectangle([(20, 20), (1260, 780)], outline=(212, 175, 55), width=2)
    draw.rectangle([(25, 25), (1255, 775)], outline=(51, 65, 85), width=1)
    
    # Header bar
    draw.rectangle([(40, 40), (1240, 110)], fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    
    # Fake browser dots
    draw.ellipse([(60, 68), (76, 84)], fill=(239, 68, 68))
    draw.ellipse([(90, 68), (106, 84)], fill=(245, 158, 11))
    draw.ellipse([(120, 68), (136, 84)], fill=(16, 185, 129))
    
    # Address bar
    draw.rounded_rectangle([(160, 58), (900, 92)], radius=8, fill=(15, 23, 42), outline=(51, 65, 85))
    try:
        font_sm = ImageFont.truetype("arial.ttf", 14)
        font_lg = ImageFont.truetype("arial.ttf", 36)
        font_sub = ImageFont.truetype("arial.ttf", 18)
    except:
        font_sm = font_lg = font_sub = ImageFont.load_default()
        
    draw.text((180, 66), f"https://auragrand.luxury/app/{tag.lower()}", fill=(148, 163, 184), font=font_sm)
    
    # Tag
    draw.rounded_rectangle([(80, 160), (340, 200)], radius=20, fill=(30, 41, 59), outline=color_accent)
    draw.text((105, 170), f"PREVIEW: {tag.upper()}", fill=color_accent, font=font_sm)
    
    # Title & Subtitle
    draw.text((80, 230), title, fill=(248, 250, 252), font=font_lg)
    draw.text((80, 290), subtitle, fill=(148, 163, 184), font=font_sub)
    
    # Center UI mockup card
    draw.rounded_rectangle([(80, 360), (1200, 720)], radius=16, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    draw.text((120, 400), "Aura Grand Hotel Room Booking Platform", fill=(212, 175, 55), font=font_sub)
    draw.line([(120, 440), (1160, 440)], fill=(51, 65, 85), width=2)
    
    # Mockup Grid
    for i in range(3):
        x = 120 + i * 360
        draw.rounded_rectangle([(x, 470), (x + 320, 680)], radius=12, fill=(15, 23, 42), outline=(71, 85, 105))
        draw.text((x + 20, 500), f"Suite Option 0{i+1}", fill=(248, 250, 252), font=font_sm)
        draw.text((x + 20, 530), "Status: Verified & Available", fill=(16, 185, 129), font=font_sm)
        draw.text((x + 20, 580), "$320.00 / night", fill=(212, 175, 55), font=font_sm)
        draw.rounded_rectangle([(x + 20, 620), (x + 300, 660)], radius=8, fill=color_accent)
        draw.text((x + 80, 630), "Select & Book", fill=(15, 23, 42), font=font_sm)
        
    img.save(path)
    print(f"Generated screenshot: {path.name}")

if __name__ == "__main__":
    create_preview_card(SCREENSHOTS_DIR / "01_Landing_Page.png", "Aura Grand - Luxury Hero & Live Search", "Interactive destinations search widget, hero banners, and portfolio showcase", "Homepage", (212, 175, 55))
    create_preview_card(SCREENSHOTS_DIR / "02_Hotels_Catalog.png", "Hotels Directory & Multi-Filter View", "Filter by region, star rating threshold, and amenities", "Hotels", (59, 130, 246))
    create_preview_card(SCREENSHOTS_DIR / "03_Suites_Booking.png", "Real-Time Room Reservation & Billing Summary", "Dynamic date quotes, promo code discounts, and secure payment modal", "Booking", (16, 185, 129))
    create_preview_card(SCREENSHOTS_DIR / "04_Guest_Reservations.png", "My Reservations & Digital Tax Invoices", "Folio emission, cancellation workflows, and status tracking", "Reservations", (217, 119, 6))

    # Also frontend image placeholders
    create_preview_card(IMAGES_DIR / "hotel_hero.png", "Grand Azure Luxury Resort", "Mediterranean beachfront 5-star hotel showcase", "Hero Image", (212, 175, 55))
    create_preview_card(IMAGES_DIR / "suite_deluxe.png", "Deluxe Ocean Suite", "King Size Bed with panoramic balcony", "Suite Image", (59, 130, 246))
