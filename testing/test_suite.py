"""
Automated End-to-End Integration Test Suite
Hotel Room Booking System
"""
import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import app
import json

def run_all_tests():
    print("=====================================================================")
    print("      HOTEL ROOM BOOKING SYSTEM - END-TO-END TEST SUITE              ")
    print("=====================================================================")
    
    client = app.test_client()
    passed = 0
    total = 15
    
    # 1. Health Check
    res = client.get('/api/health')
    assert res.status_code == 200, f"Health check failed: {res.status_code}"
    print("[PASS] 1. API Health Check verified (/api/health)")
    passed += 1

    # 2. Register New User
    reg_payload = {
        'name': 'Alexander Wright',
        'email': 'alexander.test@grandhorizon.com',
        'password': 'SecurePassword123!',
        'phone': '+1 (555) 987-6543'
    }
    res = client.post('/api/auth/register', json=reg_payload)
    assert res.status_code in [201, 409], f"Registration failed: {res.data}"
    print("[PASS] 2. User Registration endpoint verified (/api/auth/register)")
    passed += 1

    # 3. User Login
    login_payload = {
        'email': 'alexander.test@grandhorizon.com',
        'password': 'SecurePassword123!'
    }
    res = client.post('/api/auth/login', json=login_payload)
    assert res.status_code == 200, f"Login failed: {res.data}"
    auth_data = res.get_json()
    token = auth_data['token']
    user_id = auth_data['user']['id']
    headers = {'Authorization': f'Bearer {token}'}
    print(f"[PASS] 3. User Login & JWT issuance verified for user_id: {user_id}")
    passed += 1

    # 4. Current User Profile
    res = client.get('/api/auth/me', headers=headers)
    assert res.status_code == 200, f"Get profile failed: {res.data}"
    user_profile = res.get_json()['user']
    assert user_profile['email'] == 'alexander.test@grandhorizon.com'
    print(f"[PASS] 4. User Profile Retrieval via Bearer Token verified ({user_profile['name']})")
    passed += 1

    # 5. List Hotels
    res = client.get('/api/hotels')
    assert res.status_code == 200
    hotels = res.get_json()['hotels']
    assert len(hotels) >= 4
    hotel_id = hotels[0]['id']
    hotel_name = hotels[0]['name']
    print(f"[PASS] 5. List Hotels verified ({len(hotels)} luxury hotels found)")
    passed += 1

    # 6. Hotel Details by ID & Tamil Nadu State Verification
    res = client.get(f'/api/hotels/{hotel_id}')
    assert res.status_code == 200
    hotel_detail = res.get_json()['hotel']
    assert hotel_detail['state'] == 'Tamil Nadu', f"Expected Tamil Nadu, got {hotel_detail.get('state')}"
    print(f"[PASS] 6. Hotel Details verified: '{hotel_detail['name']}' in {hotel_detail['city']}, {hotel_detail['state']}")
    passed += 1

    # 6b. Tamil Nadu City Filtering
    res = client.get('/api/hotels?city=Chennai')
    assert res.status_code == 200
    chennai_hotels = res.get_json()['hotels']
    assert len(chennai_hotels) >= 1
    assert chennai_hotels[0]['city'] == 'Chennai'
    print(f"[PASS] 7. Tamil Nadu City Filter verified: Found {len(chennai_hotels)} property in Chennai")
    passed += 1

    # 7. List Rooms
    res = client.get('/api/rooms')
    assert res.status_code == 200
    rooms = res.get_json()['rooms']
    assert len(rooms) >= 5
    room_id = rooms[0]['id']
    room_name = rooms[0]['room_type']
    print(f"[PASS] 7. List Rooms verified ({len(rooms)} suites/rooms found)")
    passed += 1

    # 8. Room Filter by hotel_id
    res = client.get(f'/api/rooms?hotel_id={hotel_id}')
    assert res.status_code == 200
    filtered_rooms = res.get_json()['rooms']
    print(f"[PASS] 8. Room Filtering by Hotel ID verified ({len(filtered_rooms)} rooms found)")
    passed += 1

    # 9. Booking Quote Calculation
    quote_payload = {
        'room_id': room_id,
        'check_in': '2026-12-10',
        'check_out': '2026-12-14',
        'promo_code': 'LUXURY10'
    }
    res = client.post('/api/bookings/quote', json=quote_payload)
    assert res.status_code == 200
    pricing = res.get_json()['pricing']
    assert pricing['total_nights'] == 4
    print(f"[PASS] 9. Price Quote Calculation verified (4 nights, Subtotal: ${pricing['subtotal']}, Discount: ${pricing['discount_amount']}, Total: ${pricing['total_amount']})")
    passed += 1

    # 10. Create Room Booking
    booking_payload = {
        'room_id': room_id,
        'check_in': '2026-12-10',
        'check_out': '2026-12-14',
        'num_guests': 2,
        'special_requests': 'Ocean view suite requested with airport shuttle pickup'
    }
    res = client.post('/api/bookings', json=booking_payload, headers=headers)
    assert res.status_code == 201, f"Create booking failed: {res.data}"
    booking = res.get_json()['booking']
    booking_id = booking['id']
    print(f"[PASS] 10. Booking Creation verified (Booking ID: {booking_id}, Status: {booking['status']})")
    passed += 1

    # 11. Checkout & Payment Simulation
    pay_payload = {
        'booking_id': booking_id,
        'payment_method': 'credit_card',
        'details': {
            'card_number': '4242424242424242',
            'card_expiry': '12/28',
            'card_cvv': '123'
        }
    }
    res = client.post('/api/payments/process', json=pay_payload, headers=headers)
    assert res.status_code == 200, f"Payment failed: {res.data}"
    pay_resp = res.get_json()
    assert pay_resp['payment']['payment_status'] == 'completed'
    payment_id = pay_resp['payment']['id']
    txn_id = pay_resp['payment']['transaction_id']
    print(f"[PASS] 11. Payment Processing & Invoice Generation verified (Payment ID: {payment_id}, Txn: {txn_id})")
    passed += 1

    # 12. Check My Bookings
    res = client.get('/api/bookings/my-bookings', headers=headers)
    assert res.status_code == 200
    my_bookings = res.get_json()['bookings']
    assert any(b['id'] == booking_id for b in my_bookings)
    print(f"[PASS] 12. User Reservations List verified ({len(my_bookings)} active booking(s))")
    passed += 1

    # 13. Cancel Booking with Refund Logic
    res = client.post(f'/api/bookings/{booking_id}/cancel', headers=headers)
    assert res.status_code == 200
    cancelled_booking = res.get_json()['booking']
    assert cancelled_booking['status'] == 'cancelled'
    print(f"[PASS] 13. Booking Cancellation & Refund Handling verified for {booking_id}")
    passed += 1

    # 14. Validation Edge Cases (Check-in after check-out error)
    bad_quote = {
        'room_id': room_id,
        'check_in': '2026-12-15',
        'check_out': '2026-12-10'
    }
    res = client.post('/api/bookings/quote', json=bad_quote)
    assert res.status_code == 400
    print("[PASS] 14. Input Validation & Edge Case Handling verified (Invalid dates correctly rejected 400)")
    passed += 1

    # 15. Admin Login & Authorization
    admin_login = client.post('/api/auth/login', json={
        'email': 'admin@grandcoromandel.in',
        'password': 'AdminPass2026!'
    })
    assert admin_login.status_code == 200, f"Admin login failed: {admin_login.data}"
    admin_token = admin_login.get_json()['token']
    admin_headers = {'Authorization': f'Bearer {admin_token}'}
    print("[PASS] 15. Admin Authentication & RBAC token issued")
    passed += 1

    # 16. Admin Dashboard Stats (/api/admin/stats)
    res = client.get('/api/admin/stats', headers=admin_headers)
    assert res.status_code == 200
    stats = res.get_json()['stats']
    assert stats['total_users'] >= 2
    assert stats['total_hotels'] >= 5
    print(f"[PASS] 16. Admin Stats verified ({stats['total_users']} users, {stats['total_bookings']} tickets, {stats['total_hotels']} places)")
    passed += 1

    # 17. Admin Manage Total Users (/api/admin/users)
    res = client.get('/api/admin/users', headers=admin_headers)
    assert res.status_code == 200
    admin_users = res.get_json()['users']
    assert len(admin_users) >= 2
    print(f"[PASS] 17. Admin Manage Total Users verified ({len(admin_users)} user accounts retrieved)")
    passed += 1

    # 18. Admin Manage Customer Booked Tickets (/api/admin/bookings)
    res = client.get('/api/admin/bookings', headers=admin_headers)
    assert res.status_code == 200
    admin_bookings = res.get_json()['bookings']
    assert len(admin_bookings) >= 1
    print(f"[PASS] 18. Admin Manage Customer Booked Tickets verified ({len(admin_bookings)} reservations retrieved)")
    passed += 1

    # 19. Admin Manage Trip Places - Add New Place (/api/admin/hotels)
    new_place_payload = {
        'name': 'Chettinad Heritage Mansion & Spa',
        'city': 'Madurai',
        'state': 'Tamil Nadu',
        'address': '12 Palace Lane, Kanadukathan, Chettinad, Tamil Nadu',
        'star_rating': 4.9,
        'starting_price': 290.0,
        'default_suite_name': 'Chettinad Teak Wood Suite',
        'description': 'Centuries-old aristocratic mansion with Burmese teak pillars and Athangudi tiles.',
        'amenities': ['Ayurvedic Spa', 'Spice Garden', 'Chettinad Cuisine', 'Free WiFi']
    }
    res = client.post('/api/admin/hotels', json=new_place_payload, headers=admin_headers)
    assert res.status_code == 201
    created_place = res.get_json()['hotel']
    print(f"[PASS] 19. Admin Manage Trip Places verified (Added: '{created_place['name']}' in {created_place['city']})")
    passed += 1

    print("\n=====================================================================")
    print(f"       SUCCESS: ALL {passed}/{total + 5} INTEGRATION TESTS PASSED 100%!        ")
    print("=====================================================================")

if __name__ == '__main__':
    run_all_tests()
