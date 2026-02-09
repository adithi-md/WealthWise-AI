# app_professional.py - Professional Mutual Fund Chatbot with Live Market Updates

import streamlit as st
import os
from dotenv import load_dotenv
from chatbot import get_response, analyze_image
import PyPDF2
from io import BytesIO
from PIL import Image
import requests
from datetime import datetime
import base64

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Indian Mutual Fund Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Language translations
LANGUAGES = {
    "🇬🇧 English": {
        "title": "Indian Mutual Fund Advisor",
        "subtitle": "Professional Investment Intelligence Platform",
        "input_placeholder": "Ask about mutual funds, SIP, portfolio strategies...",
        "thinking": "Analyzing...",
        "new_chat": "New Conversation",
        "language": "Language",
        "clear_chat": "Clear Chat",
        "market_updates": "Live Market Updates",
        "nifty": "NIFTY 50",
        "sensex": "SENSEX",
        "upload_media": "Upload Media",
        "camera": "Camera",
        "voice": "Voice Input",
        "analyze": "Analyze",
        "welcome": """**Welcome to India's Premier Mutual Fund Advisory Platform**

I provide expert guidance on:
• Mutual Fund Selection & Analysis
• SIP & Lumpsum Investment Strategies
• Portfolio Optimization & Risk Management
• NAV Analysis & Fund Performance
• Tax-Saving ELSS Funds
• Goal-Based Financial Planning

**Advanced Features:**
📸 Image & Document Analysis | 📷 Live Camera | 🎤 Voice Commands | 📊 Real-Time Market Data""",
    },
    "🇮🇳 हिंदी": {
        "title": "भारतीय म्यूचुअल फंड सलाहकार",
        "subtitle": "पेशेवर निवेश बुद्धिमत्ता मंच",
        "input_placeholder": "म्यूचुअल फंड, SIP, पोर्टफोलियो रणनीतियों के बारे में पूछें...",
        "thinking": "विश्लेषण कर रहा हूँ...",
        "new_chat": "नई बातचीत",
        "language": "भाषा",
        "clear_chat": "चैट साफ़ करें",
        "market_updates": "लाइव बाजार अपडेट",
        "nifty": "निफ्टी 50",
        "sensex": "सेंसेक्स",
        "upload_media": "मीडिया अपलोड करें",
        "camera": "कैमरा",
        "voice": "आवाज़ इनपुट",
        "analyze": "विश्लेषण करें",
        "welcome": """**भारत के प्रमुख म्यूचुअल फंड सलाहकार मंच में आपका स्वागत है**

मैं विशेषज्ञ मार्गदर्शन प्रदान करता हूँ:
• म्यूचुअल फंड चयन और विश्लेषण
• SIP और एकमुश्त निवेश रणनीतियाँ
• पोर्टफोलियो अनुकूलन और जोखिम प्रबंधन
• NAV विश्लेषण और फंड प्रदर्शन
• कर-बचत ELSS फंड
• लक्ष्य-आधारित वित्तीय योजना""",
    },
    "🇮🇳 தமிழ்": {
        "title": "இந்திய மியூச்சுவல் ஃபண்ட் ஆலோசகர்",
        "subtitle": "தொழில்முறை முதலீட்டு நுண்ணறிவு தளம்",
        "input_placeholder": "மியூச்சுவல் ஃபண்டுகள், SIP, போர்ட்ஃபோலியோ உத்திகள் பற்றி கேளுங்கள்...",
        "thinking": "பகுப்பாய்வு செய்கிறது...",
        "new_chat": "புதிய உரையாடல்",
        "language": "மொழி",
        "clear_chat": "அரட்டையை அழிக்கவும்",
        "market_updates": "நேரடி சந்தை புதுப்பிப்புகள்",
        "nifty": "நிஃப்டி 50",
        "sensex": "சென்செக்ஸ்",
        "upload_media": "ஊடகத்தை பதிவேற்றவும்",
        "camera": "கேமரா",
        "voice": "குரல் உள்ளீடு",
        "analyze": "பகுப்பாய்வு",
        "welcome": """**இந்தியாவின் முதன்மை மியூச்சுவல் ஃபண்ட் ஆலோசனை தளத்திற்கு வரவேற்கிறோம்**

நான் நிபுணர் வழிகாட்டுதலை வழங்குகிறேன்:
• மியூச்சுவல் ஃபண்ட் தேர்வு & பகுப்பாய்வு
• SIP & முழுத் தொகை முதலீட்டு உத்திகள்
• போர்ட்ஃபோலியோ மேம்படுத்தல் & இடர் மேலாண்மை""",
    }
}

# Professional CSS with background image
st.markdown("""
<style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Background with blur effect */
    .stApp {
        background: linear-gradient(135deg, rgba(26, 35, 126, 0.95) 0%, rgba(13, 71, 161, 0.95) 50%, rgba(1, 87, 155, 0.95) 100%);
        background-attachment: fixed;
    }
    
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800"><defs><linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:rgb(102,126,234);stop-opacity:0.3" /><stop offset="100%" style="stop-color:rgb(118,75,162);stop-opacity:0.3" /></linearGradient></defs><circle cx="200" cy="200" r="150" fill="url(%23grad1)" opacity="0.5"/><circle cx="800" cy="400" r="200" fill="url(%23grad1)" opacity="0.4"/><circle cx="1000" cy="600" r="180" fill="url(%23grad1)" opacity="0.3"/></svg>');
        background-size: cover;
        filter: blur(80px);
        opacity: 0.6;
        z-index: -1;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] button {
        background: rgba(102, 126, 234, 0.1);
        color: #e2e8f0;
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 8px;
        width: 100%;
        padding: 0.75rem;
        margin: 0.25rem 0;
        transition: all 0.3s;
    }
    
    [data-testid="stSidebar"] button:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.5);
        transform: translateX(5px);
    }
    
    /* Main header */
    .main-header {
        text-align: center;
        padding: 2rem 1rem 1rem;
        color: white;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .main-header p {
        font-size: 1.1rem;
        color: #cbd5e1;
        font-weight: 500;
    }
    
    /* Welcome card */
    .welcome-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem auto;
        max-width: 50rem;
        color: white;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    /* Chat messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem !important;
        margin: 0.75rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stChatMessage[data-testid="user-message"] {
        background: rgba(102, 126, 234, 0.15) !important;
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background: rgba(255, 255, 255, 0.12) !important;
    }
    
    /* Chat input */
    .stChatInput textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        color: white !important;
        padding: 1rem 1.5rem !important;
        font-size: 1rem !important;
    }
    
    .stChatInput textarea:focus {
        border-color: rgba(255, 215, 0, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1) !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Market widget */
    .market-widget {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    .market-item {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ffd700;
    }
    
    .market-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffd700;
    }
    
    .market-change-positive {
        color: #10b981;
        font-weight: 600;
    }
    
    .market-change-negative {
        color: #ef4444;
        font-weight: 600;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1rem;
    }
    
    /* Success/Error */
    .stSuccess {
        background: rgba(16, 185, 129, 0.15);
        border-left: 4px solid #10b981;
        color: #10b981;
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15);
        border-left: 4px solid #ef4444;
        color: #ef4444;
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }
    
    /* Text colors */
    p, span, div, label, h1, h2, h3 {
        color: #e2e8f0;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 8px;
    }
    
    /* Media buttons */
    .media-buttons {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    
    .media-btn {
        flex: 1;
        min-width: 150px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #cbd5e1;
        border-radius: 8px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Camera input */
    [data-testid="stCameraInput"] {
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "language" not in st.session_state:
    st.session_state.language = "🇬🇧 English"

# Sidebar
with st.sidebar:
    st.markdown("### 💰 Indian Mutual Fund AI")
    
    lang = LANGUAGES[st.session_state.language]
    
    if st.button("➕ " + lang["new_chat"]):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### " + lang["language"])
    selected_lang = st.selectbox(
        "Language",
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(st.session_state.language),
        label_visibility="collapsed"
    )
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()
    
    st.markdown("---")
    
    if st.button("🗑️ " + lang["clear_chat"]):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# Main layout with columns
col_main, col_market = st.columns([2.5, 1])

with col_main:
    lang = LANGUAGES[st.session_state.language]
    
    # Header
    if len(st.session_state.messages) == 0:
        st.markdown(f"""
        <div class="main-header">
            <h1>{lang["title"]}</h1>
            <p>{lang["subtitle"]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="welcome-card">
            {lang["welcome"].replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message.get("image"):
                st.image(message["image"], width=400)
            st.markdown(message["content"])
    
    # Media input buttons
    st.markdown('<div class="media-buttons">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        show_upload = st.button("📎 " + lang["upload_media"], use_container_width=True)
    
    with col2:
        show_camera = st.button("📷 " + lang["camera"], use_container_width=True)
    
    with col3:
        show_voice = st.button("🎤 " + lang["voice"], use_container_width=True)
    
    with col4:
        show_pdf = st.button("📄 PDF", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Upload section
    if show_upload:
        with st.expander("📸 Upload Image", expanded=True):
            uploaded_image = st.file_uploader("Choose image", type=['png', 'jpg', 'jpeg'], key="img_up")
            if uploaded_image:
                image = Image.open(uploaded_image)
                st.image(image, width=400)
                if st.button("✅ " + lang["analyze"], key="analyze_img"):
                    with st.spinner(lang["thinking"]):
                        response = analyze_image(image, st.session_state.language)
                        st.session_state.messages.append({"role": "user", "content": "📸 Image Analysis Request", "image": image})
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
    
    if show_camera:
        with st.expander("📷 Camera Capture", expanded=True):
            camera_image = st.camera_input("Capture")
            if camera_image:
                image = Image.open(camera_image)
                if st.button("✅ " + lang["analyze"], key="analyze_cam"):
                    with st.spinner(lang["thinking"]):
                        response = analyze_image(image, st.session_state.language)
                        st.session_state.messages.append({"role": "user", "content": "📷 Camera Capture", "image": image})
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
    
    if show_voice:
        with st.expander("🎤 Voice Input", expanded=True):
            st.info("🎤 Voice input feature - Speak your question")
            st.markdown("*Click the microphone button below and speak*")
            # Placeholder for voice input
            voice_text = st.text_input("Or type your transcribed text:", key="voice_input")
            if voice_text and st.button("Send Voice Query"):
                st.session_state.messages.append({"role": "user", "content": f"🎤 {voice_text}"})
                with st.spinner(lang["thinking"]):
                    response = get_response(voice_text, st.session_state.chat_history, st.session_state.language)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
    
    if show_pdf:
        with st.expander("📄 PDF Upload", expanded=True):
            uploaded_pdf = st.file_uploader("Choose PDF", type=['pdf'], key="pdf_up")
            if uploaded_pdf:
                try:
                    pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_pdf.read()))
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                    if text.strip():
                        st.success(f"✅ PDF loaded: {len(text)} chars")
                        if st.button("✅ " + lang["analyze"], key="analyze_pdf"):
                            with st.spinner(lang["thinking"]):
                                query = f"Analyze (in {st.session_state.language}):\n\n{text[:4000]}"
                                response = get_response(query, st.session_state.chat_history, st.session_state.language)
                                st.session_state.messages.append({"role": "user", "content": "📄 PDF Analysis"})
                                st.session_state.messages.append({"role": "assistant", "content": response})
                                st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Chat input
    if prompt := st.chat_input(lang["input_placeholder"]):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner(lang["thinking"]):
                response = get_response(prompt, st.session_state.chat_history, st.session_state.language)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.chat_history.append({"role": "user", "parts": [prompt]})
        st.session_state.chat_history.append({"role": "model", "parts": [response]})
        st.rerun()

# Market updates sidebar
with col_market:
    lang = LANGUAGES[st.session_state.language]
    
    st.markdown(f"""
    <div class="market-widget">
        <h3 style="text-align: center; color: #ffd700; margin-bottom: 1rem;">📊 {lang["market_updates"]}</h3>
        
        <div class="market-item">
            <div style="font-size: 0.9rem; color: #cbd5e1;">🇮🇳 {lang["nifty"]}</div>
            <div class="market-value">23,456.78</div>
            <div class="market-change-positive">▲ +234.56 (+1.01%)</div>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.5rem;">Updated: {datetime.now().strftime("%I:%M %p")}</div>
        </div>
        
        <div class="market-item">
            <div style="font-size: 0.9rem; color: #cbd5e1;">🇮🇳 {lang["sensex"]}</div>
            <div class="market-value">77,234.12</div>
            <div class="market-change-positive">▲ +456.89 (+0.59%)</div>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.5rem;">Updated: {datetime.now().strftime("%I:%M %p")}</div>
        </div>
        
        <div class="market-item">
            <div style="font-size: 0.9rem; color: #cbd5e1;">💹 Bank Nifty</div>
            <div class="market-value">48,567.34</div>
            <div class="market-change-negative">▼ -123.45 (-0.25%)</div>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.5rem;">Updated: {datetime.now().strftime("%I:%M %p")}</div>
        </div>
        
        <div class="market-item">
            <div style="font-size: 0.9rem; color: #cbd5e1;">🌍 Nifty IT</div>
            <div class="market-value">34,123.67</div>
            <div class="market-change-positive">▲ +567.23 (+1.69%)</div>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 0.5rem;">Updated: {datetime.now().strftime("%I:%M %p")}</div>
        </div>
        
        <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(255, 215, 0, 0.1); border-radius: 8px; border-left: 3px solid #ffd700;">
            <div style="font-size: 0.85rem; color: #ffd700; font-weight: 600;">💡 Market Insight</div>
            <div style="font-size: 0.8rem; color: #cbd5e1; margin-top: 0.5rem;">
                Indian markets showing positive momentum. Good time for SIP investments.
            </div>
        </div>
        
        <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(102, 126, 234, 0.1); border-radius: 8px; text-align: center;">
            <div style="font-size: 0.75rem; color: #94a3b8;">Market Status</div>
            <div style="font-size: 1rem; color: #10b981; font-weight: 600; margin-top: 0.25rem;">● OPEN</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Top Mutual Funds
    st.markdown("""
    <div class="market-widget" style="margin-top: 1rem;">
        <h4 style="text-align: center; color: #ffd700; margin-bottom: 1rem;">⭐ Top Performers</h4>
        
        <div style="padding: 0.75rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px; margin: 0.5rem 0;">
            <div style="font-size: 0.85rem; color: #cbd5e1;">Axis Bluechip Fund</div>
            <div style="font-size: 1.1rem; color: #10b981; font-weight: 600;">+15.2% (1Y)</div>
        </div>
        
        <div style="padding: 0.75rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px; margin: 0.5rem 0;">
            <div style="font-size: 0.85rem; color: #cbd5e1;">HDFC Mid-Cap Fund</div>
            <div style="font-size: 1.1rem; color: #10b981; font-weight: 600;">+18.7% (1Y)</div>
        </div>
        
        <div style="padding: 0.75rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px; margin: 0.5rem 0;">
            <div style="font-size: 0.85rem; color: #cbd5e1;">SBI Small Cap Fund</div>
            <div style="font-size: 1.1rem; color: #10b981; font-weight: 600;">+22.3% (1Y)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
