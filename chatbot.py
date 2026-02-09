# chatbot.py

import os
import google.generativeai as genai
from domain_guard import is_mutual_fund_query
from prompts import SYSTEM_PROMPT, get_language_instruction
from PIL import Image

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize model with correct model name (using latest available)
model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",  # Updated to available model
    system_instruction=SYSTEM_PROMPT
)

# Vision model for image analysis
vision_model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash"
)

def get_response(user_query: str, chat_history=None, language="English") -> str:
    """
    Generates a response ONLY if the query is related to mutual funds.
    Maintains chat history for context-aware conversations.
    Supports multilingual responses.
    """
    if not is_mutual_fund_query(user_query):
        refusal_messages = {
            "English": (
                "I'm here specifically to help with **mutual funds and investment planning**.\n\n"
                "Please ask a question related to SIPs, mutual funds, returns, risk, or portfolio planning."
            ),
            "हिंदी (Hindi)": (
                "मैं विशेष रूप से **म्यूचुअल फंड और निवेश योजना** में मदद के लिए यहाँ हूँ।\n\n"
                "कृपया SIP, म्यूचुअल फंड, रिटर्न, जोखिम, या पोर्टफोलियो योजना से संबंधित प्रश्न पूछें।"
            ),
            "தமிழ் (Tamil)": (
                "நான் குறிப்பாக **மியூச்சுவல் ஃபண்டுகள் மற்றும் முதலீட்டு திட்டமிடல்** உதவிக்காக இங்கே இருக்கிறேன்.\n\n"
                "தயவுசெய்து SIP, மியூச்சுவல் ஃபண்டுகள், வருமானம், இடர் அல்லது போர்ட்ஃபோலியோ திட்டமிடல் தொடர்பான கேள்வியைக் கேளுங்கள்."
            )
        }
        return refusal_messages.get(language, refusal_messages["English"])

    try:
        # Add language instruction to the query
        lang_instruction = get_language_instruction(language)
        enhanced_query = f"{lang_instruction}\n\nUser Query: {user_query}"
        
        # Start chat session with history if provided
        if chat_history and len(chat_history) > 0:
            chat = model.start_chat(history=chat_history)
            response = chat.send_message(enhanced_query)
        else:
            response = model.generate_content(enhanced_query)
        
        return response.text

    except Exception as e:
        error_msg = str(e)
        
        # Provide helpful error messages
        if "404" in error_msg or "not found" in error_msg:
            return "⚠️ **API Configuration Issue**\n\nThe AI model is currently unavailable. Please check:\n1. Your API key is valid\n2. You have access to Gemini API\n3. Try refreshing the page\n\nError: Model not found"
        elif "quota" in error_msg.lower():
            return "⚠️ **API Quota Exceeded**\n\nYou've reached the API usage limit. Please try again later or check your Google AI Studio quota."
        elif "api key" in error_msg.lower():
            return "⚠️ **API Key Error**\n\nPlease check your GEMINI_API_KEY in the .env file."
        else:
            return f"⚠️ **Temporary Issue**\n\nI'm having trouble processing your request. Please try again.\n\nTechnical details: {error_msg[:100]}"


def analyze_image(image: Image.Image, language="English") -> str:
    """
    Analyzes uploaded images (charts, graphs, fund documents) using Gemini Vision.
    Only processes mutual fund related content.
    """
    try:
        lang_instruction = get_language_instruction(language)
        
        prompt = f"""{lang_instruction}

You are a mutual fund investment advisor. Analyze this image carefully.

If the image contains:
- Mutual fund charts, graphs, or performance data → Provide detailed analysis
- Fund fact sheets or documents → Summarize key information
- NAV trends or portfolio allocation → Explain the insights
- Any mutual fund related visual data → Provide educational commentary

If the image is NOT related to mutual funds:
- Politely decline and redirect to mutual fund topics

Provide a professional, educational analysis."""

        response = vision_model.generate_content([prompt, image])
        return response.text
        
    except Exception as e:
        error_msg = str(e)
        
        if "404" in error_msg or "not found" in error_msg:
            return "⚠️ **Image Analysis Unavailable**\n\nThe vision model is currently unavailable. Please try again later."
        else:
            return f"⚠️ **Image Analysis Error**\n\nCouldn't analyze the image. Please try:\n1. A different image\n2. Smaller file size\n3. Different format (PNG/JPG)\n\nError: {error_msg[:100]}"
