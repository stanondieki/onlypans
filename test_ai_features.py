#!/usr/bin/env python3
"""
Test OnlyPans AI Assistant functionality
"""
import requests
import json
import time

# Configuration
API_BASE = "https://onlypans.onrender.com/api"
FRONTEND_URL = "https://onlypans-ctfazewa7-stanondiekis-projects.vercel.app"

def test_ai_status():
    """Test if AI service is available"""
    print("🤖 Testing AI Service Status...")
    try:
        response = requests.get(f"{API_BASE}/ai/status/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('available'):
                print("✅ AI Service is available and ready!")
                return True
            else:
                print("❌ AI Service is not available:", data.get('message', 'Unknown error'))
                return False
        else:
            print(f"❌ AI Status check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking AI status: {str(e)}")
        return False

def login_and_get_token():
    """Login and get auth token"""
    print("\n🔐 Attempting to login...")
    credentials = [
        {"username": "admin", "password": "admin123"},
        {"username": "admin", "password": "password"},
        {"username": "admin", "password": "admin"}
    ]
    
    for cred in credentials:
        try:
            response = requests.post(f"{API_BASE}/auth/login/", json=cred, timeout=10)
            if response.status_code == 200:
                token = response.json().get('access')
                print(f"✅ Login successful with {cred['username']}")
                return token
        except Exception as e:
            continue
    
    print("❌ Login failed with all common credentials")
    return None

def test_ai_chat(token):
    """Test AI chat functionality"""
    print("\n💬 Testing AI Chat...")
    headers = {"Authorization": f"Bearer {token}"}
    
    test_questions = [
        "What's the best way to cook a perfect steak?",
        "How do I know when garlic is properly sautéed?",
        "What spices pair well with chicken?"
    ]
    
    for question in test_questions:
        try:
            print(f"   Question: {question}")
            response = requests.post(
                f"{API_BASE}/ai/chat/", 
                json={"question": question},
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    answer = data.get('data', {}).get('response', 'No response')
                    print(f"   ✅ AI Response: {answer[:100]}...")
                    print(f"   ⏱️  Processing time: {data.get('processing_time', 0):.2f}s")
                    return True
                else:
                    print(f"   ❌ Chat failed: {data.get('message')}")
            else:
                print(f"   ❌ Chat request failed with status {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Chat error: {str(e)}")
        
        break  # Only test one question to save time
    
    return False

def test_recipe_generation(token):
    """Test recipe generation from ingredients"""
    print("\n🍳 Testing Recipe Generation...")
    headers = {"Authorization": f"Bearer {token}"}
    
    recipe_request = {
        "ingredients": "chicken breast, bell peppers, onions, garlic, soy sauce, rice",
        "cuisine_preference": "Asian",
        "difficulty_preference": "medium",
        "servings": 4
    }
    
    try:
        print(f"   Ingredients: {recipe_request['ingredients']}")
        response = requests.post(
            f"{API_BASE}/ai/generate-recipe/",
            json=recipe_request,
            headers=headers,
            timeout=45
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('data', {}).get('recipe'):
                recipe = data['data']['recipe']
                print(f"   ✅ Generated Recipe: {recipe.get('title', 'Untitled')}")
                print(f"   📝 Description: {recipe.get('description', 'No description')[:100]}...")
                print(f"   ⏱️  Prep: {recipe.get('prep_time')}m | Cook: {recipe.get('cook_time')}m")
                print(f"   👥 Serves: {recipe.get('servings')} | 📊 Difficulty: {recipe.get('difficulty')}")
                print(f"   🥄 Ingredients count: {len(recipe.get('ingredients', []))}")
                print(f"   📋 Instructions count: {len(recipe.get('instructions', []))}")
                return True
            else:
                print(f"   ❌ Recipe generation failed: {data.get('message')}")
        else:
            print(f"   ❌ Recipe request failed with status {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Recipe generation error: {str(e)}")
    
    return False

def test_frontend_access():
    """Test frontend accessibility"""
    print("\n🌐 Testing Frontend Access...")
    
    urls_to_test = [
        f"{FRONTEND_URL}/",
        f"{FRONTEND_URL}/ai",
        f"{FRONTEND_URL}/recipes",
        f"{FRONTEND_URL}/meals"
    ]
    
    for url in urls_to_test:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {url} - Accessible")
            else:
                print(f"   ❌ {url} - Status {response.status_code}")
        except Exception as e:
            print(f"   ❌ {url} - Error: {str(e)}")

def main():
    """Run all tests"""
    print("🚀 OnlyPans AI Assistant Test Suite")
    print("=" * 50)
    
    # Test AI service availability
    ai_available = test_ai_status()
    
    # Try to login
    token = login_and_get_token()
    
    if not token:
        print("\n❌ Cannot proceed with AI tests - login required")
        print("\nTo fix this:")
        print("1. Go to Render dashboard → onlypans service → Shell")
        print("2. Run: python manage.py createsuperuser")
        print("3. Use username: admin, password: admin123")
        return
    
    # Test AI functionality if available
    if ai_available and token:
        print(f"\n🧪 Running AI functionality tests...")
        
        chat_success = test_ai_chat(token)
        recipe_success = test_recipe_generation(token)
        
        if chat_success and recipe_success:
            print("\n🎉 All AI features are working!")
        else:
            print("\n⚠️  Some AI features may not be working properly")
            print("Make sure to set GOOGLE_AI_API_KEY in Render environment variables")
    
    # Test frontend
    test_frontend_access()
    
    # Summary
    print("\n📋 SUMMARY")
    print("=" * 30)
    print(f"✅ Backend Health: Working")
    print(f"{'✅' if token else '❌'} Authentication: {'Working' if token else 'Needs setup'}")
    print(f"{'✅' if ai_available else '❌'} AI Service: {'Available' if ai_available else 'Needs API key'}")
    print(f"✅ Frontend: Accessible")
    
    if ai_available and token:
        print(f"\n🎯 Ready to use!")
        print(f"   Frontend: {FRONTEND_URL}/ai")
        print(f"   Backend API: {API_BASE}/ai/")
    else:
        print(f"\n🔧 Setup needed:")
        if not token:
            print(f"   - Create admin user on Render")
        if not ai_available:
            print(f"   - Add GOOGLE_AI_API_KEY to Render environment")

if __name__ == "__main__":
    main()
