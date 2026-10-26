# 🚀 Hotel Room Booking System — Complete Startup Guide

This document explains how to start and run the **Backend API** and **Frontend Web Application**, explains the directory navigation rules, and provides solutions to common command-line errors.

---

## ⚠️ Why Did the Previous Command Fail?

When you ran:
```powershell
Command: python backend/app.py
CWD: e:\HOTEL ROOM BOOKING SYSTEM\backend
Error: can't open file '.../backend/backend/app.py': No such file or directory
```

### The Reason:
Your PowerShell terminal was **already inside** the `backend` folder (`CWD: e:\HOTEL ROOM BOOKING SYSTEM\backend`).
When you typed `python backend/app.py`, Windows looked for:
$$\text{e:\HOTEL ROOM BOOKING SYSTEM\backend} + \text{\backend\app.py} = \text{backend\backend\app.py (does not exist)}$$

---

## 🎯 How to Run (Choose Any Method Below)

---

### Method 1: The Easiest Way — 1-Click Root Launcher (Recommended)

From the project root directory (`e:\HOTEL ROOM BOOKING SYSTEM`):

```powershell
python run.py
```
*Or on Windows: simply double-click **`start.bat`** in File Explorer!*

This starts the Flask server, which serves **both** the REST API and the frontend web pages together at:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

### Method 2: Running from the Project Root

If your terminal prompt shows `e:\HOTEL ROOM BOOKING SYSTEM`:

```powershell
# 1. Make sure you are in the root directory:
cd "e:\HOTEL ROOM BOOKING SYSTEM"

# 2. Run the application:
python backend/app.py
```

---

### Method 3: Running from Inside the `backend` Folder

If your terminal prompt shows `e:\HOTEL ROOM BOOKING SYSTEM\backend`:

```powershell
# If you are already inside the backend folder:
python app.py
```

*(Notice: it is just `python app.py`, **not** `python backend/app.py`)*

To go back to the root folder at any time:
```powershell
cd ..
```

---

### Method 4: Running Backend & Frontend in Two Separate Terminals

If you prefer to run the Backend and Frontend on separate independent ports:

#### Terminal 1: Start Backend (Port 5000)
```powershell
cd "e:\HOTEL ROOM BOOKING SYSTEM"
python backend/app.py
```
* Backend API runs at: **`http://127.0.0.1:5000/api`**

#### Terminal 2: Start Frontend (Port 3000)
Open a new terminal window:
```powershell
cd "e:\HOTEL ROOM BOOKING SYSTEM"
python -m http.server 3000 --directory frontend
```
* Open your browser at: **`http://127.0.0.1:3000`**
* The client script (`frontend/js/main.js`) will automatically connect to `http://127.0.0.1:5000/api`!

---

## 🌐 Application URLs & Pages

Once the server is running, open your web browser to any of these addresses:

| Page / Feature | URL | Description |
|---|---|---|
| **Landing Page** | [http://127.0.0.1:5000/](http://127.0.0.1:5000/) | Luxury search bar, hero banner, featured retreats |
| **Hotels Catalog** | [http://127.0.0.1:5000/hotels.html](http://127.0.0.1:5000/hotels.html) | Filter Tamil Nadu properties by city & rating |
| **Suites & Rooms** | [http://127.0.0.1:5000/rooms.html](http://127.0.0.1:5000/rooms.html) | View suites, villas, nightly pricing & capacity |
| **Booking & Checkout** | [http://127.0.0.1:5000/booking.html](http://127.0.0.1:5000/booking.html) | Live pricing calculator, promo codes & payment |
| **My Reservations** | [http://127.0.0.1:5000/my_bookings.html](http://127.0.0.1:5000/my_bookings.html) | View booked stays, download folios, cancel |
| **Member Sign-in** | [http://127.0.0.1:5000/login.html](http://127.0.0.1:5000/login.html) | Quick-autofill buttons for Guest and Admin |
| **API Health Check** | [http://127.0.0.1:5000/api/health](http://127.0.0.1:5000/api/health) | JSON API health status indicator |

---

## 🧪 How to Run Automated Tests

To run the automated 15-point end-to-end integration test suite:

```powershell
cd "e:\HOTEL ROOM BOOKING SYSTEM"
python testing/test_suite.py
```

All 15 tests should report `[PASS]` with a 100% success summary.

---

## 🔑 Demo Account Credentials

Use these pre-configured test credentials to sign in:

* **Guest User:**
  - Email: `sophia@example.com`
  - Password: `password123`

* **Admin User:**
  - Email: `admin@grandcoromandel.in`
  - Password: `AdminPass2026!`

---

## 🔧 Troubleshooting Common Errors

### 1. `Error: [Errno 2] No such file or directory`
* **Fix:** Check where you are by running `pwd` (PowerShell) or `cd` (Command Prompt).
  - If you are in `e:\HOTEL ROOM BOOKING SYSTEM`: run `python run.py` or `python backend/app.py`.
  - If you are in `e:\HOTEL ROOM BOOKING SYSTEM\backend`: run `python app.py`.

### 2. `Address already in use` or Port 5000 busy
* **Fix:** A background server is already running on port 5000! You can open [http://127.0.0.1:5000](http://127.0.0.1:5000) directly in your browser.
* If you want to stop the existing process:
  ```powershell
  # Find process on port 5000:
  Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Select-Object OwningProcess
  # Stop it:
  Stop-Process -Id <PID> -Force
  ```

### 3. Missing Dependencies
* If you receive `ModuleNotFoundError: No module named 'flask'`:
  ```powershell
  pip install -r requirements.txt
  ```
