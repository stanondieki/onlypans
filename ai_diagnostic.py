#!/usr/bin/env python3
"""
Diagnose AI Assistant Issues
"""
import requests
import json

BASE_URL = "https://onlypans.onrender.com/api"

def check_ai_status():
    """Check AI service availability"""
    print("🔍 Checking AI Service Status...")
    try:
        response = requests.get(f"{BASE_URL}/ai/status/", timeout=20)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            return data.get('available', False)
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_login():
    """Test admin login"""
    print("\n🔐 Testing Admin Login...")
    try:
        data = {"username": "admin", "password": "admin123"}
        response = requests.post(f"{BASE_URL}/auth/login/", json=data, timeout=20)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            token = result.get('access', '')
            print("✅ Login successful!")
            return token
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_ai_chat(token):
    """Test AI chat with authentication"""
    print("\n💬 Testing AI Chat...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        data = {"question": "Hello, can you help me with cooking?"}
        
        response = requests.post(f"{BASE_URL}/ai/chat/", json=data, headers=headers, timeout=30)
        print(f"Chat Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            return result.get('success', False)
        return False
    except Exception as e:
        print(f"❌ AI Chat error: {e}")
        return False

def main():
    print("=" * 50)
    print("🚨 AI Assistant Diagnostic Tool")
    print("=" * 50)
    
    # Step 1: Check AI service
    ai_available = check_ai_status()
    
    # Step 2: Test login
    token = test_login()
    
    # Step 3: Test AI chat if login works
    ai_chat_works = False
    if token:
        ai_chat_works = test_ai_chat(token)
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSTIC RESULTS")
    print("=" * 50)
    print(f"AI Service Available: {'✅ YES' if ai_available else '❌ NO'}")
    print(f"Admin Login Works:    {'✅ YES' if token else '❌ NO'}")
    print(f"AI Chat Works:        {'✅ YES' if ai_chat_works else '❌ NO'}")
    
    print("\n🔧 TROUBLESHOOTING:")
    
    if not ai_available:
        print("❌ AI Service Issue:")
        print("   1. Check if GOOGLE_API_KEY is set in Render environment")
        print("   2. Verify your Gemini API key is valid")
        print("   3. Check Render logs for errors")
    
    if not token:
        print("❌ Authentication Issue:")
        print("   1. Superuser might not be created")
        print("   2. Try different password")
        print("   3. Check if environment variables are set")
    
    if token and not ai_chat_works:
        print("❌ AI Chat Issue:")
        print("   1. API key might be invalid")
        print("   2. Check backend logs")
        print("   3. Verify network connectivity")

if __name__ == "__main__":
    main()
