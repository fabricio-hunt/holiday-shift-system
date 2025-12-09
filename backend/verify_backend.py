import requests
import uuid
from datetime import date
import logging

logging.basicConfig(level=logging.INFO)

BASE_URL = "http://127.0.0.1:8080"

def test_endpoints():
    try:
        # 1. Test Root
        print("Testing Root Endpoint...")
        resp = requests.get(f"{BASE_URL}/")
        print(f"Root: {resp.status_code} - {resp.json()}")
        if resp.status_code != 200: return False

        # 2. Test Debug
        print("\nTesting Debug Endpoint...")
        resp = requests.get(f"{BASE_URL}/debug")
        print(f"Debug: {resp.status_code} - {resp.json()}")
        if resp.status_code != 200: return False

        # 3. Test Get Shifts
        print("\nTesting Get Shifts...")
        resp = requests.get(f"{BASE_URL}/shifts")
        print(f"Get Shifts: {resp.status_code} - {resp.json()}")
        if resp.status_code != 200: return False

        # 4. Test Create Shift
        print("\nTesting Create Shift...")
        new_shift = {
            "name": "Test Employee",
            "holiday_date": str(date.today())
        }
        # Auth is mocked/hardcoded in auth.py? 
        # Looking at main.py, it uses Depends(get_current_username) which uses HTTPBasic
        # We need to provide credentials.
        # auth.py was viewed earlier, let's check if we need auth for POST/DELETE.
        # main.py: @app.post("/shifts", dependencies=[Depends(get_current_username)])
        # We need to send auth headers.
        
        auth = requests.auth.HTTPBasicAuth("admin", "Bemol@2025")
        
        resp = requests.post(f"{BASE_URL}/shifts", json=new_shift, auth=auth)
        print(f"Create Shift: {resp.status_code} - {resp.text}")
        if resp.status_code != 200: return False
        created_shift = resp.json()
        shift_id = created_shift["id"]

        # 5. Test Delete Shift
        print(f"\nTesting Delete Shift ({shift_id})...")
        resp = requests.delete(f"{BASE_URL}/shifts/{shift_id}", auth=auth)
        print(f"Delete Shift: {resp.status_code} - {resp.json()}")
        if resp.status_code != 200: return False

        print("\nALL TESTS PASSED")
        return True

    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        return False

if __name__ == "__main__":
    test_endpoints()
