#!/usr/bin/env python3
"""
Test login functionality with different credentials
"""
import requests
import json

BASE_URL = "https://onlypans.onrender.com/api"

def test_login(username, password):
    """Test login with given credentials"""
    print(f"Testing login: {username}")
    data = {"username": username, "password": password}
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=data, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ LOGIN SUCCESS!")
            print(f"Access Token: {result.get('access', '')[:50]}...")
            return result.get('access')
        else:
            print("❌ LOGIN FAILED")
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

def main():
    print("=== Testing Login Credentials ===\n")
    
    # Common credential combinations to test
    credentials = [
        ("admin", "admin123"),
        ("admin", "admin"),
        ("adminonly", "admin123"),
        ("adminonly", "admin"),
        ("ondie", "admin123"),
        ("ondie", "admin"),
    ]
    
    working_creds = []
    
    for username, password in credentials:
        token = test_login(username, password)
        if token:
            working_creds.append((username, password))
        print("-" * 50)
    
    print("\n=== SUMMARY ===")
    if working_creds:
        print("✅ Working credentials found:")
        for username, password in working_creds:
            print(f"   Username: {username}, Password: {password}")
    else:
        print("❌ No working credentials found")
        print("\n🔧 Solutions:")
        print("1. Create superuser on Render using the shell")
        print("2. Check if you remember the correct password")
        print("3. Reset password if needed")

if __name__ == "__main__":
    main()
