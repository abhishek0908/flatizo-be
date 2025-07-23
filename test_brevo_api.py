#!/usr/bin/env python3
"""
Test script to verify Brevo API connectivity
"""
import asyncio
import httpx
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

async def test_brevo_api():
    BREVO_API_KEY = os.getenv("BREVO_API_KEY")
    BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
    
    if not BREVO_API_KEY:
        print("❌ BREVO_API_KEY not found!")
        return
    
    # Test payload (minimal)
    payload = {
        "sender": {"name": "Test", "email": "test@example.com"},
        "to": [{"email": "test@example.com", "name": "Test User"}],
        "subject": "Test Email",
        "htmlContent": "<p>Test</p>",
    }
    
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
    }
    
    print("=== Testing Brevo API ===")
    print(f"API URL: {BREVO_API_URL}")
    print(f"API Key: {BREVO_API_KEY[:10]}...{BREVO_API_KEY[-10:]}")
    
    try:
        timeout = httpx.Timeout(30.0, connect=10.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            # First, let's test account info endpoint to verify API key
            account_url = "https://api.brevo.com/v3/account"
            account_response = await client.get(account_url, headers={"api-key": BREVO_API_KEY})
            
            print(f"\n=== Account Info Test ===")
            print(f"Status: {account_response.status_code}")
            
            if account_response.status_code == 200:
                print("✅ API Key is valid!")
                account_data = account_response.json()
                print(f"Account Email: {account_data.get('email', 'N/A')}")
                print(f"Plan: {account_data.get('plan', {}).get('type', 'N/A')}")
            else:
                print("❌ API Key validation failed!")
                print(f"Response: {account_response.text}")
                
    except httpx.ReadTimeout:
        print("❌ Request timed out")
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP Error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_brevo_api())
