# test_chat.py - Quick test of chatbot functionality

import os
from dotenv import load_dotenv
from chatbot import get_response

load_dotenv()

print("Testing Mutual Fund Chatbot...")
print("="*50)

# Test queries
test_queries = [
    "What is SIP?",
    "Explain mutual funds",
    "What is NAV?",
    "Tell me about Bitcoin"  # Should be rejected
]

for query in test_queries:
    print(f"\n📝 Query: {query}")
    print("-" * 50)
    try:
        response = get_response(query, None, "English")
        print(f"🤖 Response: {response[:200]}...")
        print("✅ SUCCESS")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    print()

print("="*50)
print("Test complete! If you see responses above, the chatbot is working!")
