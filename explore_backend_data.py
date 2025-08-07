#!/usr/bin/env python3
"""
OnlyPans Backend Data Explorer
View your backend data through API endpoints
"""
import requests
import json
from datetime import datetime

BASE_URL = "https://onlypans.onrender.com/api"

def login_and_get_token():
    """Login and get access token"""
    print("🔐 Logging in...")
    try:
        data = {"username": "admin", "password": "admin123"}
        response = requests.post(f"{BASE_URL}/auth/login/", json=data, timeout=10)
        
        if response.status_code == 200:
            token = response.json().get('access')
            print("✅ Login successful!")
            return token
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def get_data(endpoint, token, description):
    """Get data from an endpoint"""
    print(f"\n📊 {description}...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data.get('results', data)) if isinstance(data, dict) else len(data)} items")
            return data
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def display_data(data, title, limit=5):
    """Display data in a readable format"""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print('='*60)
    
    if not data:
        print("No data found.")
        return
    
    # Handle paginated responses
    items = data.get('results', data) if isinstance(data, dict) else data
    
    if not isinstance(items, list):
        items = [items]
    
    for i, item in enumerate(items[:limit]):
        print(f"\n{i+1}. ", end="")
        
        # Display different types of data appropriately
        if isinstance(item, dict):
            # For recipes
            if 'title' in item:
                print(f"Recipe: {item.get('title', 'Untitled')}")
                if 'description' in item:
                    print(f"   Description: {item.get('description', '')[:100]}...")
                if 'created_at' in item:
                    print(f"   Created: {item.get('created_at', '')}")
                if 'ai_generated' in item:
                    print(f"   AI Generated: {item.get('ai_generated', False)}")
            
            # For AI requests
            elif 'request_type' in item:
                print(f"AI Request: {item.get('request_type', 'Unknown')}")
                if 'input_text' in item:
                    print(f"   Input: {item.get('input_text', '')[:100]}...")
                if 'response_text' in item:
                    response = item.get('response_text', '')
                    print(f"   Response: {response[:100]}..." if len(response) > 100 else f"   Response: {response}")
                if 'created_at' in item:
                    print(f"   Created: {item.get('created_at', '')}")
            
            # For users
            elif 'username' in item:
                print(f"User: {item.get('username', '')}")
                if 'email' in item:
                    print(f"   Email: {item.get('email', '')}")
                if 'is_superuser' in item:
                    print(f"   Superuser: {item.get('is_superuser', False)}")
                if 'date_joined' in item:
                    print(f"   Joined: {item.get('date_joined', '')}")
            
            # For meals
            elif 'meal_type' in item:
                print(f"Meal: {item.get('meal_type', 'Unknown')} - {item.get('scheduled_date', '')}")
                if 'recipe' in item:
                    print(f"   Recipe: {item.get('recipe', {}).get('title', 'No recipe')}")
            
            # Generic display for other items
            else:
                for key, value in list(item.items())[:3]:
                    print(f"   {key}: {str(value)[:50]}...")
        else:
            print(str(item)[:100])
    
    if len(items) > limit:
        print(f"\n... and {len(items) - limit} more items")

def main():
    print("🗄️  OnlyPans Backend Data Explorer")
    print("="*60)
    
    # Login first
    token = login_and_get_token()
    if not token:
        print("❌ Cannot explore data without authentication")
        return
    
    # Define data endpoints to explore
    endpoints = [
        ("/recipes/", "All Recipes"),
        ("/recipes/my-recipes/", "My Recipes"),
        ("/ai/requests/", "AI Requests History"),
        ("/meals/plans/", "Meal Plans"),
        ("/auth/stats/", "User Statistics"),
        ("/ai/stats/", "AI Usage Statistics"),
    ]
    
    # Fetch and display data from each endpoint
    for endpoint, description in endpoints:
        data = get_data(endpoint, token, description)
        if data:
            display_data(data, description)
    
    print(f"\n{'='*60}")
    print("🌐 Additional Ways to View Data:")
    print("1. Django Admin: https://onlypans.onrender.com/admin/")
    print("2. API Browser: https://onlypans.onrender.com/api/")
    print("3. Frontend Dashboard: Your app's dashboard page")
    print("="*60)

if __name__ == "__main__":
    main()
