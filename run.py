"""
Root Launcher Script for Hotel Room Booking System
Serves both Backend API and Frontend UI.
"""
import sys
import os
from pathlib import Path

# Ensure root directory is on Python path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app import app
from backend.config import Config

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    import webbrowser
    import threading

    # Automatically open browser once server is ready
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not Config.DEBUG:
        threading.Timer(1.2, lambda: webbrowser.open(f"http://127.0.0.1:{port}")).start()

    print("==================================================")
    print("  HOTEL ROOM BOOKING SYSTEM IS RUNNING!")
    print("==================================================")
    print(f"  * Web Application : http://127.0.0.1:{port}")
    print(f"  * Admin Portal    : http://127.0.0.1:{port}/admin.html")
    print(f"  * Hotels Catalog  : http://127.0.0.1:{port}/hotels.html")
    print(f"  * Suites Directory: http://127.0.0.1:{port}/rooms.html")
    print(f"  * API Health Check: http://127.0.0.1:{port}/api/health")
    print("==================================================")
    print("  The server is active. Keep this terminal open!")
    print("  Opening browser automatically...")
    print("  Press Ctrl+C to stop the server.")
    print("==================================================")
    app.run(host="0.0.0.0", port=port, debug=Config.DEBUG)
