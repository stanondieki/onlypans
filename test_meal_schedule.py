#!/usr/bin/env python3
"""
Test script to create meal plan data for testing the meal schedule view
"""
import requests
import json
from datetime import datetime, timedelta

# Configuration
API_BASE = "https://onlypans.onrender.com/api"
USERNAME = "admin"
PASSWORD = "admin123"

def login():
    """Login and get token"""
    response = requests.post(f"{API_BASE}/accounts/login/", {
        "username": USERNAME,
        "password": PASSWORD
    })
    if response.status_code == 200:
        return response.json()["access"]
    else:
        print(f"Login failed: {response.text}")
        return None

def create_test_meal_plan(token):
    """Create a test meal plan for this week"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get current week dates
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())  # Monday
    week_end = week_start + timedelta(days=6)  # Sunday
    
    meal_plan_data = {
        "name": "Test Week Meal Plan",
        "start_date": week_start.isoformat(),
        "end_date": week_end.isoformat(),
        "is_active": True
    }
    
    response = requests.post(f"{API_BASE}/meals/plans/", 
                           json=meal_plan_data, headers=headers)
    if response.status_code == 201:
        plan = response.json()
        print(f"Created meal plan: {plan['name']} (ID: {plan['id']})")
        return plan
    else:
        print(f"Failed to create meal plan: {response.text}")
        return None

def get_recipes(token):
    """Get available recipes"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE}/recipes/", headers=headers)
    if response.status_code == 200:
        recipes = response.json()
        if 'results' in recipes:
            return recipes['results']
        return recipes
    return []

def create_test_meals(token, meal_plan_id, recipes):
    """Create some test meals for the meal plan"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get current week dates
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())  # Monday
    
    meals_to_create = []
    
    # Create meals for the week
    for day_offset in range(7):
        meal_date = week_start + timedelta(days=day_offset)
        
        # Breakfast
        if len(recipes) > 0:
            meals_to_create.append({
                "recipe": recipes[0]["id"],
                "date": meal_date.isoformat(),
                "meal_type": "breakfast",
                "servings": 2,
                "notes": f"Breakfast for {meal_date.strftime('%A')}"
            })
        
        # Lunch (every other day)
        if day_offset % 2 == 0 and len(recipes) > 1:
            meals_to_create.append({
                "recipe": recipes[1]["id"],
                "date": meal_date.isoformat(),
                "meal_type": "lunch",
                "servings": 1,
                "notes": f"Lunch for {meal_date.strftime('%A')}"
            })
        
        # Dinner (most days)
        if day_offset < 5 and len(recipes) > 2:
            recipe_idx = min(2 + (day_offset % 3), len(recipes) - 1)
            meals_to_create.append({
                "recipe": recipes[recipe_idx]["id"],
                "date": meal_date.isoformat(),
                "meal_type": "dinner",
                "servings": 3,
                "notes": f"Dinner for {meal_date.strftime('%A')}"
            })
    
    # Create the meals
    created_meals = []
    for meal_data in meals_to_create:
        response = requests.post(f"{API_BASE}/meals/plans/{meal_plan_id}/meals/", 
                               json=meal_data, headers=headers)
        if response.status_code == 201:
            meal = response.json()
            created_meals.append(meal)
            print(f"Created {meal['meal_type']} for {meal['date']}")
        else:
            print(f"Failed to create meal: {response.text}")
    
    return created_meals

def test_date_range_api(token):
    """Test the new date range API"""
    headers = {"Authorization": f"Bearer {token}"}
    
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    response = requests.get(
        f"{API_BASE}/meals/by-date/?start_date={week_start.isoformat()}&end_date={week_end.isoformat()}", 
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Date range API test successful!")
        print(f"Found {len(data['meals'])} meals for the week")
        print(f"Date range: {data['date_range']['start_date']} to {data['date_range']['end_date']}")
        
        # Show meals by day
        meals_by_day = {}
        for meal in data['meals']:
            date = meal['date']
            if date not in meals_by_day:
                meals_by_day[date] = []
            meals_by_day[date].append(f"{meal['meal_type']}: {meal['recipe_details']['title'] if meal['recipe_details'] else 'Unknown recipe'}")
        
        for date, meal_list in sorted(meals_by_day.items()):
            day_name = datetime.fromisoformat(date).strftime('%A')
            print(f"  {day_name} ({date}):")
            for meal in meal_list:
                print(f"    - {meal}")
        
        return True
    else:
        print(f"❌ Date range API test failed: {response.text}")
        return False

def main():
    print("🚀 Setting up meal schedule test data...")
    
    # Login
    token = login()
    if not token:
        print("❌ Failed to login")
        return
    
    print("✅ Logged in successfully")
    
    # Get available recipes
    recipes = get_recipes(token)
    if not recipes:
        print("❌ No recipes found. Please run the init_onlypans command first.")
        return
    
    print(f"✅ Found {len(recipes)} recipes")
    
    # Create meal plan
    meal_plan = create_test_meal_plan(token)
    if not meal_plan:
        return
    
    # Create test meals
    meals = create_test_meals(token, meal_plan["id"], recipes)
    print(f"✅ Created {len(meals)} meals")
    
    # Test the date range API
    test_date_range_api(token)
    
    print("\n🎉 Test setup complete! You can now test the meal schedule view.")
    print(f"   Frontend: https://onlypans-ctfazewa7-stanondiekis-projects.vercel.app/meals")
    print(f"   Backend API: {API_BASE}/meals/by-date/")

if __name__ == "__main__":
    main()
