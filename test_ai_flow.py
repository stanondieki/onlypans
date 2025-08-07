import requests
import json

def test_ai_complete_flow():
    BASE_URL = "https://onlypans.onrender.com/api"
    
    print("🔧 Testing Complete AI Flow...\n")
    
    # Step 1: Test AI Status
    print("1️⃣ Testing AI Service Status...")
    try:
        response = requests.get(f"{BASE_URL}/ai/status/", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            ai_available = data.get('available', False)
            print(f"   AI Available: {ai_available}")
            print(f"   Message: {data.get('message', '')}")
            
            if not ai_available:
                print("   ❌ AI service not available - check GOOGLE_API_KEY")
                return False
        else:
            print(f"   ❌ Bad status: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Step 2: Test Login
    print("\n2️⃣ Testing Login...")
    try:
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json().get('access')
            print("   ✅ Login successful!")
            print(f"   Token: {token[:30]}...")
        else:
            print(f"   ❌ Login failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return False
    
    # Step 3: Test AI Chat
    print("\n3️⃣ Testing AI Recipe Generation...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        question = "Can you give me a simple recipe for chocolate chip cookies?"
        
        response = requests.post(
            f"{BASE_URL}/ai/chat/", 
            json={"question": question}, 
            headers=headers, 
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                ai_response = result.get('data', {}).get('response', '')
                print("   ✅ AI Response generated!")
                print(f"   Preview: {ai_response[:150]}...")
                print(f"   Full response length: {len(ai_response)} characters")
                return True
            else:
                print(f"   ❌ AI response failed: {result.get('message')}")
                return False
        else:
            print(f"   ❌ Request failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ AI chat error: {e}")
        return False

def main():
    print("🤖 OnlyPans AI Integration Test")
    print("=" * 50)
    
    success = test_ai_complete_flow()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SUCCESS! Your AI integration is working!")
        print("\n📝 Next steps:")
        print("1. Login to your frontend with admin/admin123")
        print("2. Go to AI Assistant page")
        print("3. Ask cooking questions and get AI responses!")
    else:
        print("❌ AI integration needs fixes")
        print("\n🔧 Common solutions:")
        print("1. Add GOOGLE_API_KEY to Render environment variables")
        print("2. Make sure API key is valid and has quota")
        print("3. Wait 2-3 minutes after adding key for deployment")
        print("4. Check Render logs for errors")

if __name__ == "__main__":
    main()
