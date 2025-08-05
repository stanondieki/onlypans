import requests
import json

BASE_URL = 'http://localhost:8000/api'

def test_api_endpoints():
    print("Testing OnlyPans API endpoints...\n")
    
    # Test recipe list endpoint
    print("1. Testing Recipe List Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/recipes/")
        if response.status_code == 200:
            recipes = response.json()
            print(f"✅ Found {len(recipes['results']) if 'results' in recipes else len(recipes)} recipes")
            if recipes['results'] if 'results' in recipes else recipes:
                first_recipe = recipes['results'][0] if 'results' in recipes else recipes[0]
                print(f"   First recipe: {first_recipe['title']}")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test recipe tags endpoint
    print("\n2. Testing Recipe Tags Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/recipes/tags/")
        if response.status_code == 200:
            tags = response.json()
            print(f"✅ Found {len(tags)} tags")
            if tags:
                tag_names = [tag['name'] for tag in tags[:5]]
                print(f"   Sample tags: {', '.join(tag_names)}")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test user registration
    print("\n3. Testing User Registration Endpoint")
    try:
        user_data = {
            "username": "testapi",
            "email": "testapi@onlypans.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "first_name": "API",
            "last_name": "Test"
        }
        response = requests.post(f"{BASE_URL}/auth/register/", json=user_data)
        if response.status_code == 201:
            user = response.json()
            print(f"✅ User registered successfully: {user['username']}")
        elif response.status_code == 400 and 'already exists' in str(response.json()):
            print("✅ User already exists (expected)")
        else:
            print(f"❌ Failed with status {response.status_code}: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test user login
    print("\n4. Testing User Login Endpoint")
    try:
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        if response.status_code == 200:
            tokens = response.json()
            print("✅ Login successful")
            print(f"   Access token starts with: {tokens['access'][:20]}...")
            
            # Test authenticated endpoint
            print("\n5. Testing Authenticated Endpoint (User Profile)")
            headers = {'Authorization': f"Bearer {tokens['access']}"}
            profile_response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
            
            if profile_response.status_code == 200:
                profile = profile_response.json()
                print(f"✅ Profile retrieved for user: {profile['user']['username']}")
            else:
                print(f"❌ Profile request failed with status {profile_response.status_code}")
        else:
            print(f"❌ Login failed with status {response.status_code}: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test AI service status
    print("\n6. Testing AI Service Status")
    try:
        response = requests.get(f"{BASE_URL}/ai/status/")
        if response.status_code == 200:
            status_data = response.json()
            print(f"✅ AI Service Available: {status_data['available']}")
            print(f"   Message: {status_data['message']}")
        else:
            print(f"❌ Failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*50)
    print("API Testing Complete!")
    print("Backend is ready for frontend integration.")

if __name__ == '__main__':
    test_api_endpoints()
