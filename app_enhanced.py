# app_enhanced.py - Enhanced ChatGPT-style UI with full multimodal support

import streamlit as st
import os
from dotenv import load_dotenv
from chatbot import get_response, analyze_image
import PyPDF2
from io import BytesIO
from PIL import Image
from audio_recorder_streamlit import audio_recorder

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Mutual Fund AI Advisor",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Language translations
LANGUAGES = {
    "🇬🇧 English": {
        "title": "Mutual Fund AI Advisor",
        "subtitle": "Your intelligent investment companion",
        "input_placeholder": "Message Mutual Fund Advisor...",
        "thinking": "Thinking...",
        "send": "Send",
        "new_chat": "New Chat",
        "settings": "Settings",
        "language": "Language",
        "clear_chat": "Clear Conversation",
        "welcome": """👋 **Hello! I'm your Mutual Fund AI Advisor.**

I can help you with:
• Understanding mutual funds & investment strategies
• SIP vs Lumpsum planning
• Risk assessment & portfolio optimization
• NAV, expense ratios, fund categories
• Goal-based investment planning

**Multimodal Capabilities:**
📄 Upload PDF documents
📸 Upload images or use camera
🎤 Voice input support

*How can I assist you today?*""",
        "refusal": "I specialize exclusively in mutual funds. Please ask about SIPs, mutual funds, returns, risk, or portfolio planning.",
        "disclaimer": "⚠️ Educational tool only. Investments subject to market risks. Consult a certified financial advisor.",
        "upload_image": "Upload Image",
        "upload_pdf": "Upload PDF",
        "use_camera": "Use Camera",
        "voice_input": "Voice Input",
        "analyze": "Analyze",
        "capture": "Capture Photo"
    },
    "🇮🇳 हिंदी": {
        "title": "म्यूचुअल फंड AI सलाहकार",
        "subtitle": "आपका बुद्धिमान निवेश साथी",
        "input_placeholder": "म्यूचुअल फंड सलाहकार को संदेश...",
        "thinking": "सोच रहा हूँ...",
        "send": "भेजें",
        "new_chat": "नई चैट",
        "settings": "सेटिंग्स",
        "language": "भाषा",
        "clear_chat": "बातचीत साफ़ करें",
        "welcome": """👋 **नमस्ते! मैं आपका म्यूचुअल फंड AI सलाहकार हूँ।**

मैं आपकी मदद कर सकता हूँ:
• म्यूचुअल फंड और निवेश रणनीतियों को समझना
• SIP बनाम एकमुश्त योजना
• जोखिम मूल्यांकन और पोर्टफोलियो अनुकूलन
• NAV, व्यय अनुपात, फंड श्रेणियाँ
• लक्ष्य-आधारित निवेश योजना

**मल्टीमॉडल क्षमताएं:**
📄 PDF दस्तावेज़ अपलोड करें
📸 छवियाँ अपलोड करें या कैमरा उपयोग करें
🎤 आवाज़ इनपुट समर्थन

*आज मैं आपकी कैसे सहायता कर सकता हूँ?*""",
        "refusal": "मैं विशेष रूप से म्यूचुअल फंड में विशेषज्ञता रखता हूँ।",
        "disclaimer": "⚠️ केवल शैक्षिक उपकरण। निवेश बाजार जोखिमों के अधीन।",
        "upload_image": "छवि अपलोड करें",
        "upload_pdf": "PDF अपलोड करें",
        "use_camera": "कैमरा उपयोग करें",
        "voice_input": "आवाज़ इनपुट",
        "analyze": "विश्लेषण करें",
        "capture": "फोटो कैप्चर करें"
    },
    "🇮🇳 தமிழ்": {
        "title": "மியூச்சுவல் ஃபண்ட் AI ஆலோசகர்",
        "subtitle": "உங்கள் அறிவார்ந்த முதலீட்டு துணை",
        "input_placeholder": "மியூச்சுவல் ஃபண்ட் ஆலோசகருக்கு செய்தி...",
        "thinking": "சிந்திக்கிறது...",
        "send": "அனுப்பு",
        "new_chat": "புதிய அரட்டை",
        "settings": "அமைப்புகள்",
        "language": "மொழி",
        "clear_chat": "உரையாடலை அழிக்கவும்",
        "welcome": """👋 **வணக்கம்! நான் உங்கள் மியூச்சுவல் ஃபண்ட் AI ஆலோசகர்.**

நான் உங்களுக்கு உதவ முடியும்:
• மியூச்சுவல் ஃபண்டுகள் & முதலீட்டு உத்திகளை புரிந்துகொள்ளுதல்
• SIP vs முழுத் தொகை திட்டமிடல்
• இடர் மதிப்பீடு & போர்ட்ஃபோலியோ மேம்படுத்தல்
• NAV, செலவு விகிதங்கள், நிதி வகைகள்
• இலக்கு அடிப்படையிலான முதலீட்டு திட்டமிடல்

**மல்டிமோடல் திறன்கள்:**
📄 PDF ஆவணங்களை பதிவேற்றவும்
📸 படங்களை பதிவேற்றவும் அல்லது கேமராவைப் பயன்படுத்தவும்
🎤 குரல் உள்ளீடு ஆதரவு

*இன்று நான் உங்களுக்கு எவ்வாறு உதவ முடியும்?*""",
        "refusal": "நான் குறிப்பாக மியூச்சுவல் ஃபண்டுகளில் நிபுணத்துவம் பெற்றவன்.",
        "disclaimer": "⚠️ கல்வி கருவி மட்டுமே. முதலீடுகள் சந்தை அபாயங்களுக்கு உட்பட்டவை.",
        "upload_image": "படத்தை பதிவேற்றவும்",
        "upload_pdf": "PDF பதிவேற்றவும்",
        "use_camera": "கேமராவைப் பயன்படுத்தவும்",
        "voice_input": "குரல் உள்ளீடு",
        "analyze": "பகுப்பாய்வு செய்யவும்",
        "capture": "புகைப்படம் எடுக்கவும்"
    }
}

# Premium ChatGPT-style CSS
st.markdown("""
<style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Dark theme */
    .stApp {
        background: #343541;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #202123;
    }
    
    [data-testid="stSidebar"] button {
        background: transparent;
        color: #ececf1;
        border: 1px solid #4d4d4f;
        border-radius: 6px;
        width: 100%;
        padding: 0.75rem;
        margin: 0.25rem 0;
        text-align: left;
        transition: background 0.2s;
    }
    
    [data-testid="stSidebar"] button:hover {
        background: #2a2b32;
    }
    
    /* Main content */
    .main-header {
        text-align: center;
        padding: 3rem 1rem 2rem;
        color: #ececf1;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1rem;
        color: #9b9b9f;
    }
    
    /* Welcome card */
    .welcome-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 2.5rem;
        margin: 2rem auto;
        max-width: 42rem;
        color: white;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }
    
    /* Chat messages */
    .stChatMessage {
        background: transparent !important;
        padding: 1.5rem 1rem !important;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .stChatMessage[data-testid="user-message"] {
        background: #343541 !important;
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background: #444654 !important;
    }
    
    /* Chat input */
    .stChatInput textarea {
        background: #40414f !important;
        border: 1px solid #565869 !important;
        border-radius: 12px !important;
        color: #ececf1 !important;
        padding: 1rem 1.5rem !important;
        font-size: 1rem !important;
    }
    
    .stChatInput textarea:focus {
        border-color: #19c37d !important;
        box-shadow: 0 0 0 3px rgba(25, 195, 125, 0.15) !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.65rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #40414f;
        border: 2px dashed #565869;
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #667eea;
        background: #4a4b57;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #40414f;
        border-radius: 8px;
        padding: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #9b9b9f;
        border-radius: 6px;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: #667eea;
        color: white;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #40414f;
        color: #ececf1;
        border-radius: 8px;
        border: 1px solid #565869;
        padding: 1rem;
    }
    
    /* Success/Error */
    .stSuccess {
        background: rgba(25, 195, 125, 0.15);
        border-left: 4px solid #19c37d;
        color: #19c37d;
        border-radius: 6px;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15);
        border-left: 4px solid #ef4444;
        color: #ef4444;
        border-radius: 6px;
    }
    
    /* Disclaimer */
    .disclaimer {
        background: rgba(251, 191, 36, 0.15);
        border-left: 4px solid #fbbf24;
        color: #fbbf24;
        padding: 1rem;
        border-radius: 6px;
        font-size: 0.9rem;
        margin: 1rem 0;
    }
    
    /* Text colors */
    p, span, div, label {
        color: #ececf1;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: #40414f;
        border: 1px solid #565869;
        color: #ececf1;
        border-radius: 8px;
    }
    
    /* Camera input */
    [data-testid="stCameraInput"] {
        border: 2px solid #565869;
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Action buttons row */
    .action-row {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    
    .action-btn {
        flex: 1;
        min-width: 120px;
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
    st.markdown("### 💰 Mutual Fund AI")
    
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
    
    st.markdown("### " + lang["settings"])
    
    if st.button("🗑️ " + lang["clear_chat"]):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")
    
    st.markdown(f'<div class="disclaimer">{lang["disclaimer"]}</div>', unsafe_allow_html=True)

# Main content
lang = LANGUAGES[st.session_state.language]

# Header (only show if no messages)
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

# Multimodal input options
st.markdown('<div class="action-row">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    show_image = st.button("📸 " + lang["upload_image"], use_container_width=True)

with col2:
    show_pdf = st.button("📄 " + lang["upload_pdf"], use_container_width=True)

with col3:
    show_camera = st.button("📷 " + lang["use_camera"], use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Image upload
if show_image:
    with st.expander("📸 " + lang["upload_image"], expanded=True):
        uploaded_image = st.file_uploader(
            "Choose an image",
            type=['png', 'jpg', 'jpeg'],
            key="image_uploader"
        )
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, width=400)
            if st.button("✅ " + lang["analyze"], key="analyze_image"):
                with st.spinner(lang["thinking"]):
                    response = analyze_image(image, st.session_state.language)
                    st.session_state.messages.append({
                        "role": "user",
                        "content": "📸 [Image uploaded for analysis]",
                        "image": image
                    })
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                    st.rerun()

# PDF upload
if show_pdf:
    with st.expander("📄 " + lang["upload_pdf"], expanded=True):
        uploaded_pdf = st.file_uploader(
            "Choose a PDF",
            type=['pdf'],
            key="pdf_uploader"
        )
        if uploaded_pdf:
            try:
                pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_pdf.read()))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                if text.strip():
                    st.success(f"✅ PDF loaded: {len(text)} characters")
                    if st.button("✅ " + lang["analyze"], key="analyze_pdf"):
                        with st.spinner(lang["thinking"]):
                            query = f"Analyze this mutual fund document (respond in {st.session_state.language}):\n\n{text[:4000]}"
                            response = get_response(query, st.session_state.chat_history, st.session_state.language)
                            st.session_state.messages.append({
                                "role": "user",
                                "content": "📄 [PDF document uploaded for analysis]"
                            })
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": response
                            })
                            st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Camera capture
if show_camera:
    with st.expander("📷 " + lang["use_camera"], expanded=True):
        camera_image = st.camera_input(lang["capture"])
        
        if camera_image:
            image = Image.open(camera_image)
            if st.button("✅ " + lang["analyze"], key="analyze_camera"):
                with st.spinner(lang["thinking"]):
                    response = analyze_image(image, st.session_state.language)
                    st.session_state.messages.append({
                        "role": "user",
                        "content": "📷 [Photo captured for analysis]",
                        "image": image
                    })
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })
                    st.rerun()

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
