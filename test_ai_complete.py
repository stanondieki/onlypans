#!/usr/bin/env python3
"""
Complete AI service test with superuser credentials
"""
import requests
import json

# Configuration
BASE_URL = "https://onlypans.onrender.com/api"

def test_ai_status():
    """Test AI service status"""
    print("🔍 Testing AI service status...")
    try:
        response = requests.get(f"{BASE_URL}/ai/status/", timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI Service Available: {data.get('available', False)}")
            print(f"📝 Message: {data.get('message', 'No message')}")
            return data.get('available', False)
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_full_ai_workflow():
    """Test complete AI workflow with authentication"""
    print("\n🧪 Testing complete AI workflow...")
    
    # Step 1: Get credentials
    username = input("Enter your superuser username (or press Enter for 'admin'): ").strip() or "admin"
    password = input("Enter your superuser password: ").strip()
    
    if not password:
        print("❌ Password is required")
        return False
    
    # Step 2: Login
    print(f"\n🔐 Logging in as {username}...")
    try:
        login_response = requests.post(
            f"{BASE_URL}/auth/login/", 
            json={"username": username, "password": password}, 
            timeout=30
        )
        
        if login_response.status_code == 200:
            token = login_response.json().get('access')
            print("✅ Login successful!")
        else:
            print(f"❌ Login failed: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Step 3: Test AI Chat
    print("\n💬 Testing AI chat...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        chat_data = {"question": "Give me a simple 3-ingredient pasta recipe"}
        
        chat_response = requests.post(
            f"{BASE_URL}/ai/chat/", 
            json=chat_data, 
            headers=headers, 
            timeout=60
        )
        
        if chat_response.status_code == 200:
            result = chat_response.json()
            if result.get('success'):
                print("✅ AI Chat working!")
                response_text = result.get('data', {}).get('response', '')
                print(f"📝 AI Response Preview: {response_text[:200]}...")
                print(f"⏱️  Processing Time: {result.get('processing_time', 'N/A')} seconds")
                return True
            else:
                print(f"❌ AI Chat failed: {result.get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ AI Chat request failed: {chat_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ AI Chat error: {e}")
        return False

def main():
    print("=== OnlyPans AI Complete Test ===")
    print("This will test your AI service after superuser creation\n")
    
    # Test 1: AI Status
    status_ok = test_ai_status()
    
    if not status_ok:
        print("\n❌ AI service is not available. Please check:")
        print("1. Your GOOGLE_API_KEY environment variable in Render")
        print("2. That your Gemini API key is valid")
        print("3. Backend deployment logs for errors")
        return
    
    # Test 2: Full workflow
    workflow_ok = test_full_ai_workflow()
    
    print("\n=== Final Results ===")
    print(f"AI Service Status: {'✅ WORKING' if status_ok else '❌ FAILED'}")
    print(f"Complete AI Workflow: {'✅ WORKING' if workflow_ok else '❌ FAILED'}")
    
    if status_ok and workflow_ok:
        print("\n🎉 SUCCESS! Your AI assistant is fully functional!")
        print("You can now use the AI features in your frontend application.")
    else:
        print("\n⚠️  Some issues remain. Check the error messages above.")

if __name__ == "__main__":
    main()
