#!/usr/bin/env python3
"""
Test script for AI service functionality
"""
import requests
import json
import sys

# Configuration
BASE_URL = "https://onlypans.onrender.com/api"

def test_ai_status():
    """Test AI service status endpoint"""
    print("Testing AI service status...")
    try:
        response = requests.get(f"{BASE_URL}/ai/status/", timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            return data.get('available', False)
        else:
            print(f"Error Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False
    except Exception as e:
        print(f"Error testing AI status: {e}")
        return False

def test_basic_connectivity():
    """Test basic API connectivity"""
    print("Testing basic API connectivity...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=30)
        print(f"API Root Status Code: {response.status_code}")
        return response.status_code in [200, 404]  # 404 is OK for API root
    except requests.exceptions.RequestException as e:
        print(f"Connectivity error: {e}")
        return False
    except Exception as e:
        print(f"Error testing connectivity: {e}")
        return False

def test_auth_endpoints():
    """Test if auth endpoints are working"""
    print("Testing auth endpoints...")
    try:
        # Test registration endpoint (expect 400 for empty data)
        response = requests.post(f"{BASE_URL}/auth/register/", json={}, timeout=30)
        print(f"Auth Register Status Code: {response.status_code}")
        return response.status_code in [400, 405]  # Expected for empty data
    except requests.exceptions.RequestException as e:
        print(f"Auth test error: {e}")
        return False
    except Exception as e:
        print(f"Error testing auth: {e}")
        return False

def test_ai_chat_with_sample_credentials():
    """Test AI chat with sample credentials"""
    print("\nTesting AI chat with sample credentials...")
    
    # Try to login with default admin credentials
    login_data = {"username": "admin", "password": "admin123"}
    
    try:
        login_response = requests.post(f"{BASE_URL}/auth/login/", json=login_data, timeout=30)
        print(f"Login Status Code: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token = login_response.json().get('access')
            print("Login successful!")
            
            # Test AI chat
            headers = {"Authorization": f"Bearer {token}"}
            chat_data = {"question": "What's a simple pasta recipe?"}
            
            chat_response = requests.post(f"{BASE_URL}/ai/chat/", json=chat_data, headers=headers, timeout=60)
            print(f"AI Chat Status Code: {chat_response.status_code}")
            
            if chat_response.status_code == 200:
                result = chat_response.json()
                print("AI Chat successful!")
                print(f"Response preview: {str(result.get('data', {}).get('response', ''))[:200]}...")
                return True
            else:
                print(f"AI Chat failed: {chat_response.text}")
                return False
        else:
            print(f"Login failed: {login_response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False
    except Exception as e:
        print(f"Error testing AI chat: {e}")
        return False

def main():
    print("=== OnlyPans AI Service Comprehensive Test ===\n")
    
    # Test 1: Basic connectivity
    connectivity_ok = test_basic_connectivity()
    
    # Test 2: Auth endpoints
    auth_ok = test_auth_endpoints()
    
    # Test 3: AI Status (no auth required)
    status_ok = test_ai_status()
    
    # Test 4: AI Chat with authentication
    chat_ok = test_ai_chat_with_sample_credentials()
    
    # Summary
    print("\n=== Comprehensive Test Summary ===")
    print(f"Basic Connectivity: {'✅ PASS' if connectivity_ok else '❌ FAIL'}")
    print(f"Auth Endpoints: {'✅ PASS' if auth_ok else '❌ FAIL'}")
    print(f"AI Status: {'✅ PASS' if status_ok else '❌ FAIL'}")
    print(f"AI Chat (Full Flow): {'✅ PASS' if chat_ok else '❌ FAIL'}")
    
    # Troubleshooting recommendations
    print("\n=== Troubleshooting Recommendations ===")
    
    if not connectivity_ok:
        print("🔧 Backend Connectivity Issues:")
        print("1. Check if the Render service is running")
        print("2. Verify the API URL is correct")
        print("3. Check for any deployment errors in Render logs")
    
    if not status_ok:
        print("🔧 AI Service Configuration Issues:")
        print("1. Check if GOOGLE_AI_API_KEY (or GOOGLE_API_KEY) is set in Render environment variables")
        print("2. Verify the Gemini API key is valid and has quota available")
        print("3. Check backend logs for any configuration errors")
        print("4. Ensure the google-generativeai package is installed")
    
    if not chat_ok:
        print("🔧 AI Chat Issues:")
        print("1. Create an admin user if it doesn't exist: python manage.py createsuperuser")
        print("2. Check authentication token generation")
        print("3. Verify AI endpoint permissions and authentication")
        print("4. Check for any AI service initialization errors")
    
    # Overall status
    if all([connectivity_ok, status_ok, chat_ok]):
        print("\n🎉 All tests passed! AI service should be working.")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        
    return 0 if all([connectivity_ok, status_ok]) else 1

if __name__ == "__main__":
    sys.exit(main())
