import requests

def test_backend():
    try:
        print("Testing backend connectivity...")
        r = requests.get('https://onlypans.onrender.com/api/ai/status/', timeout=15)
        print(f'Status: {r.status_code}')
        print(f'Response: {r.text}')
        return r.status_code == 200
    except Exception as e:
        print(f'Error: {e}')
        return False

if __name__ == "__main__":
    test_backend()
