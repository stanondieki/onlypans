#!/usr/bin/env python3
"""
Test superuser creation and login after Render deployment
"""
import requests
import json
import time

BASE_URL = "https://onlypans.onrender.com/api"

def test_api_connectivity():
    """Test basic API connectivity"""
    print("🔗 Testing API connectivity...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=30)
        print(f"   API Root Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"   ❌ Connectivity failed: {e}")
        return False

def test_ai_status():
    """Test AI service status"""
    print("🤖 Testing AI service status...")
    try:
        response = requests.get(f"{BASE_URL}/ai/status/", timeout=30)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   AI Available: {data.get('available', False)}")
            return data.get('available', False)
        else:
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ AI status check failed: {e}")
        return False

def test_superuser_login():
    """Test superuser login"""
    print("👤 Testing superuser login...")
    
    credentials = [
        ("admin", "admin123"),
        ("admin", "admin"),
    ]
    
    for username, password in credentials:
        try:
            print(f"   Trying: {username}/{password}")
            data = {"username": username, "password": password}
            response = requests.post(f"{BASE_URL}/auth/login/", json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ LOGIN SUCCESS with {username}")
                token = result.get('access', '')
                print(f"   Token: {token[:50]}...")
                return token
            else:
                print(f"   ❌ Failed: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None

def test_ai_chat(token):
    """Test AI chat functionality"""
    print("💬 Testing AI chat...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        data = {"question": "What's a simple recipe for scrambled eggs?"}
        
        response = requests.post(f"{BASE_URL}/ai/chat/", json=data, headers=headers, timeout=60)
        print(f"   Chat Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                ai_response = result.get('data', {}).get('response', '')
                print(f"   ✅ AI Response (preview): {ai_response[:100]}...")
                return True
            else:
                print(f"   ❌ AI Chat failed: {result.get('message', 'Unknown error')}")
        else:
            print(f"   ❌ Request failed: {response.text}")
        
        return False
    except Exception as e:
        print(f"   ❌ AI chat error: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 OnlyPans Deployment Test - Complete System Check")
    print("=" * 60)
    
    # Test 1: Basic connectivity
    connectivity = test_api_connectivity()
    print()
    
    # Test 2: AI Service Status
    ai_status = test_ai_status()
    print()
    
    # Test 3: Superuser login
    token = test_superuser_login()
    print()
    
    # Test 4: AI Chat (if login successful)
    ai_chat_works = False
    if token:
        ai_chat_works = test_ai_chat(token)
        print()
    
    # Summary
    print("=" * 60)
    print("📊 FINAL RESULTS")
    print("=" * 60)
    print(f"API Connectivity:     {'✅ PASS' if connectivity else '❌ FAIL'}")
    print(f"AI Service Available: {'✅ PASS' if ai_status else '❌ FAIL'}")
    print(f"Superuser Login:      {'✅ PASS' if token else '❌ FAIL'}")
    print(f"AI Chat Function:     {'✅ PASS' if ai_chat_works else '❌ FAIL'}")
    
    if token and ai_status and ai_chat_works:
        print("\n🎉 SUCCESS! Your OnlyPans app is fully functional!")
        print("\n📝 Next Steps:")
        print("1. Visit your frontend: https://onlypans-ctfazewa7-stanondiekis-projects.vercel.app")
        print("2. Login with: admin / admin123")
        print("3. Navigate to AI Assistant and start cooking!")
    elif token and not ai_status:
        print("\n⚠️  Login works but AI needs configuration!")
        print("💡 Add your GOOGLE_API_KEY environment variable in Render")
    elif not token:
        print("\n❌ Superuser creation failed!")
        print("💡 Check Render logs or try the API endpoint method")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
