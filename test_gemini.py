# test_gemini.py - Test Gemini API connection

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Testing Gemini API...")
print(f"API Key loaded: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")
print()

# List available models
print("Available models:")
try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")
    print()

# Test with different model names
model_names = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-pro",
    "models/gemini-1.5-flash",
    "models/gemini-pro"
]

print("\nTesting models:")
for model_name in model_names:
    try:
        print(f"\nTrying: {model_name}")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'Hello' in one word")
        print(f"  ✅ SUCCESS: {response.text}")
        print(f"  Use this model: {model_name}")
        break
    except Exception as e:
        print(f"  ❌ Failed: {str(e)[:100]}")

print("\n" + "="*50)
print("Test complete!")
