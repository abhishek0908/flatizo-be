#!/usr/bin/env python3
"""
Test script to verify environment variables are loaded correctly
"""
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Check if BREVO_API_KEY is loaded
brevo_key = os.getenv("BREVO_API_KEY")

print("=== Environment Variable Test ===")
print(f"BREVO_API_KEY exists: {brevo_key is not None}")
if brevo_key:
    print(f"BREVO_API_KEY length: {len(brevo_key)} characters")
    print(f"BREVO_API_KEY starts with: {brevo_key[:10]}...")
else:
    print("❌ BREVO_API_KEY is not set or empty!")
    print("\nTo fix this:")
    print("1. Add BREVO_API_KEY=your_api_key_here to your .env file")
    print("2. Get your API key from https://app.brevo.com/settings/keys/api")

print("\n=== All Environment Variables ===")
for key, value in os.environ.items():
    if 'BREVO' in key.upper() or 'API' in key.upper():
        print(f"{key}: {'*' * len(value) if value else 'NOT SET'}")
