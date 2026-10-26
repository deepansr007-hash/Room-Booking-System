import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "luxury-hotel-booking-secret-key-2026")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-luxury-hotel-secret-key-998877")
    JWT_ACCESS_TOKEN_EXPIRES_HOURS = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 24))
    
    # Database
    DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
    DATABASE_PATH = BASE_DIR / os.getenv("DATABASE_PATH", "database/hotel_booking.db")
    SAMPLE_DATA_PATH = BASE_DIR / "database" / "sample_data.json"
    PERSISTENT_DATA_PATH = BASE_DIR / "database" / "active_database.json"
    
    # Frontend directory for serving static assets and pages
    FRONTEND_DIR = BASE_DIR / "frontend"
    
    # Payment simulation
    PAYMENT_GATEWAY_ENV = os.getenv("PAYMENT_GATEWAY_ENV", "sandbox")
    MOCK_PAYMENT_SUCCESS_RATE = float(os.getenv("MOCK_PAYMENT_SUCCESS_RATE", 0.98))
    
    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
