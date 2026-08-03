import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GOOGLE_AI_STUDIO_KEY", "")
model = "gemma-4-26b-a4b-it"

print("=" * 60)
print("Checking your setup...")
print("=" * 60)

if not api_key or api_key == "your-google-ai-studio-api-key":
    print(" GOOGLE_AI_STUDIO_KEY is missing or still the placeholder value.")
    print("   Go to https://aistudio.google.com/apikey, create a key,")
    print("   and paste it into your .env file.")
    exit(1)
else:
    print(f"Found an API key (starts with: {api_key[:6]}...)")

print()
print("Calling Gemma with a test message...")
print()

import requests

url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

payload = {
    "contents": [
        {"role": "user", "parts": [{"text": "Say hello in one short sentence."}]}
    ]
}

response = requests.post(url, params={"key": api_key}, json=payload, timeout=20)

print(f"Status code: {response.status_code}")
print()
print("Full response:")
print(response.text)