import requests
import json

# Login
login_data = {'username': 'test@studywiseai.com', 'password': 'testpass123'}
login_resp = requests.post('http://localhost:8000/api/auth/login', data=login_data)
print(f"Login Status: {login_resp.status_code}")

if login_resp.status_code == 200:
    token = login_resp.json()['access_token']
    print(f"Token obtained: {token[:20]}...")
    
    # Call career counseling
    headers = {'Authorization': f'Bearer {token}'}
    career_data = {'target_profession': 'Software Engineer'}
    
    career_resp = requests.post(
        'http://localhost:8000/api/ai/career-counseling/start',
        json=career_data,
        headers=headers
    )
    print(f"\nCareer Counseling Status: {career_resp.status_code}")
    print(f"Response: {career_resp.text[:1000]}")
else:
    print(f"Login failed: {login_resp.text}")
