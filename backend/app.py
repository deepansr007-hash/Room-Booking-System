import os
import sys
from pathlib import Path

# Ensure root directory is on Python path
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from backend.config import Config
from backend.routes.auth_routes import auth_bp
from backend.routes.hotel_routes import hotel_bp
from backend.routes.room_routes import room_bp
from backend.routes.booking_routes import booking_bp
from backend.routes.payment_routes import payment_bp
from backend.routes.admin_routes import admin_bp

def create_app():
    app = Flask(
        __name__,
        static_folder=str(Config.FRONTEND_DIR),
        static_url_path=""
    )
    app.config.from_object(Config)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}})

    # Register API Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(hotel_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(admin_bp)

    # API Health Check
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "Hotel Room Booking System API",
            "version": "1.0.0",
            "environment": os.getenv("FLASK_ENV", "development")
        }), 200

    # Frontend Page Serving
    @app.route("/")
    def serve_index():
        return send_from_directory(Config.FRONTEND_DIR, "index.html")

    @app.route("/<path:path>")
    def serve_frontend_file(path):
        target_path = Config.FRONTEND_DIR / path
        if target_path.exists() and not target_path.is_dir():
            return send_from_directory(Config.FRONTEND_DIR, path)
        
        # If accessing without .html extension (e.g. /login, /hotels)
        html_candidate = Config.FRONTEND_DIR / f"{path}.html"
        if html_candidate.exists():
            return send_from_directory(Config.FRONTEND_DIR, f"{path}.html")

        # Fallback to index.html for client navigation if applicable
        if not path.startswith("api/"):
            return send_from_directory(Config.FRONTEND_DIR, "index.html")

        return jsonify({"success": False, "message": "API endpoint not found."}), 404

    # Global Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "message": "Resource not found"}), 404
        return send_from_directory(Config.FRONTEND_DIR, "index.html")

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"success": False, "message": "Internal server error"}), 500

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    import webbrowser
    import threading

    # Automatically open browser once server is ready
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not Config.DEBUG:
        threading.Timer(1.2, lambda: webbrowser.open(f"http://127.0.0.1:{port}")).start()

    print(f"==================================================")
    print(f"  HOTEL ROOM BOOKING SYSTEM IS RUNNING!")
    print(f"==================================================")
    print(f"  * Web Application : http://127.0.0.1:{port}")
    print(f"  * Admin Portal    : http://127.0.0.1:{port}/admin.html")
    print(f"  * Hotels Catalog  : http://127.0.0.1:{port}/hotels.html")
    print(f"  * Suites Directory: http://127.0.0.1:{port}/rooms.html")
    print(f"  * API Health Check: http://127.0.0.1:{port}/api/health")
    print(f"==================================================")
    print(f"  The server is active. Keep this terminal open!")
    print(f"  Opening browser automatically...")
    print(f"  Press Ctrl+C to stop the server.")
    print(f"==================================================")
    app.run(host="0.0.0.0", port=port, debug=Config.DEBUG)
