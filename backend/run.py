"""
Backend directory forwarder:
Allows running 'python run.py' directly even when inside the backend/ folder.
"""
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKEND_DIR.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Run the root launcher
if __name__ == "__main__":
    from run import app, Config
    import os
    import webbrowser
    import threading

    port = int(os.getenv("PORT", 5000))
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
