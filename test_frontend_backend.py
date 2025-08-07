import requests
import json

def test_frontend_backend_connection():
    print("🔍 Testing Frontend-Backend Connection Issues")
    print("=" * 60)
    
    BASE_URL = "https://onlypans.onrender.com/api"
    FRONTEND_URL = "https://onlypans-ctfazewa7-stanondiekis-projects.vercel.app"
    
    # Test 1: Backend Health
    print("1️⃣ Testing Backend Health...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        print(f"   Backend Status: {response.status_code}")
        if response.status_code in [200, 404]:  # 404 is OK for API root
            print("   ✅ Backend is reachable")
        else:
            print(f"   ❌ Backend issue: {response.text}")
    except Exception as e:
        print(f"   ❌ Backend unreachable: {e}")
        return False
    
    # Test 2: CORS Configuration
    print("\n2️⃣ Testing CORS Configuration...")
    try:
        # Simulate a preflight request
        headers = {
            'Origin': FRONTEND_URL,
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type,Authorization'
        }
        response = requests.options(f"{BASE_URL}/auth/login/", headers=headers, timeout=10)
        print(f"   CORS Preflight Status: {response.status_code}")
        
        cors_headers = response.headers
        if 'Access-Control-Allow-Origin' in cors_headers:
            print(f"   ✅ CORS Allow Origin: {cors_headers['Access-Control-Allow-Origin']}")
        else:
            print("   ❌ CORS headers missing")
            
    except Exception as e:
        print(f"   ❌ CORS test failed: {e}")
    
    # Test 3: Authentication Flow
    print("\n3️⃣ Testing Authentication Flow...")
    try:
        login_data = {"username": "admin", "password": "admin123"}
        headers = {'Origin': FRONTEND_URL}
        
        response = requests.post(
            f"{BASE_URL}/auth/login/", 
            json=login_data, 
            headers=headers,
            timeout=10
        )
        
        print(f"   Login Status: {response.status_code}")
        if response.status_code == 200:
            token = response.json().get('access')
            print("   ✅ Authentication working")
            return token
        else:
            print(f"   ❌ Login failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Auth test failed: {e}")
        return None

def test_ai_endpoints(token):
    print("\n4️⃣ Testing AI Endpoints with Authentication...")
    BASE_URL = "https://onlypans.onrender.com/api"
    FRONTEND_URL = "https://onlypans-ctfazewa7-stanondiekis-projects.vercel.app"
    
    if not token:
        print("   ❌ No token available for testing")
        return False
    
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Origin': FRONTEND_URL,
            'Content-Type': 'application/json'
        }
        
        # Test AI Chat endpoint
        chat_data = {"question": "Hello, can you help me with a simple recipe?"}
        response = requests.post(
            f"{BASE_URL}/ai/chat/", 
            json=chat_data,
            headers=headers,
            timeout=30
        )
        
        print(f"   AI Chat Status: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("   ✅ AI Chat working correctly")
                print(f"   Response preview: {str(result.get('data', {}).get('response', ''))[:100]}...")
                return True
            else:
                print(f"   ❌ AI Chat failed: {result.get('message', 'Unknown error')}")
        else:
            print(f"   ❌ AI endpoint error: {response.text}")
            
        return False
        
    except Exception as e:
        print(f"   ❌ AI test error: {e}")
        return False

def check_frontend_config():
    print("\n5️⃣ Checking Frontend Configuration...")
    
    # Check if frontend environment variables are correct
    expected_backend = "https://onlypans.onrender.com/api"
    print(f"   Expected Backend URL: {expected_backend}")
    print(f"   Frontend URL: https://onlypans-ctfazewa7-stanondiekis-projects.vercel.app")
    
    print("\n   🔧 Frontend Environment Check:")
    print("   - NEXT_PUBLIC_API_URL should be: https://onlypans.onrender.com/api")
    print("   - Check Vercel environment variables")

def provide_troubleshooting():
    print("\n" + "=" * 60)
    print("🔧 TROUBLESHOOTING GUIDE")
    print("=" * 60)
    
    print("\n📋 Common Frontend-Backend Issues:")
    
    print("\n1️⃣ CORS Issues:")
    print("   - Frontend domain not in CORS_ALLOWED_ORIGINS")
    print("   - Missing credentials in requests")
    print("   - Preflight requests failing")
    
    print("\n2️⃣ Environment Variables:")
    print("   - NEXT_PUBLIC_API_URL not set correctly in Vercel")
    print("   - Backend URL pointing to wrong endpoint")
    
    print("\n3️⃣ Authentication Issues:")
    print("   - Token not being sent with requests")
    print("   - Token expiring quickly")
    print("   - Login not persisting")
    
    print("\n4️⃣ Network Issues:")
    print("   - Backend sleeping (Render free tier)")
    print("   - Slow response times causing timeouts")
    print("   - Browser blocking mixed content")
    
    print("\n🛠️ Quick Fixes to Try:")
    print("   1. Clear browser cache completely")
    print("   2. Check browser console for JavaScript errors")
    print("   3. Try in incognito/private browser window")
    print("   4. Verify you're logged in before testing AI")
    print("   5. Check Network tab in browser dev tools")

def main():
    print("🚨 Frontend-Backend Connection Diagnostic")
    print("=" * 60)
    
    # Run tests
    token = test_frontend_backend_connection()
    ai_working = test_ai_endpoints(token)
    check_frontend_config()
    
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    print(f"Backend Reachable: {'✅' if token else '❌'}")
    print(f"Authentication: {'✅' if token else '❌'}")  
    print(f"AI Endpoints: {'✅' if ai_working else '❌'}")
    
    if token and ai_working:
        print("\n🎉 Backend is working perfectly!")
        print("❗ Issue is likely in frontend configuration or browser")
        print("\n📝 Next Steps:")
        print("1. Check browser console for JavaScript errors")
        print("2. Verify NEXT_PUBLIC_API_URL in Vercel")
        print("3. Clear browser cache and cookies")
        print("4. Test in different browser")
    else:
        print("\n❌ Backend issues detected")
        
    provide_troubleshooting()

if __name__ == "__main__":
    main()
