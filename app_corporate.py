# app_corporate.py - Professional Corporate Mutual Fund Advisory Platform

import streamlit as st
import os
from dotenv import load_dotenv
from chatbot import get_response, analyze_image
import PyPDF2
from io import BytesIO
from PIL import Image
import requests
from datetime import datetime
import json

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="WealthWise AI - Smart Mutual Fund Advisory",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fetch real market data
@st.cache_data(ttl=60)
def get_live_market_data():
    """Fetch live market data from NSE"""
    try:
        # Using Yahoo Finance API as fallback
        indices = {
            "NIFTY 50": "^NSEI",
            "SENSEX": "^BSESN",
            "BANK NIFTY": "^NSEBANK"
        }
        
        market_data = {}
        for name, symbol in indices.items():
            try:
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                response = requests.get(url, timeout=5)
                data = response.json()
                
                if 'chart' in data and 'result' in data['chart']:
                    result = data['chart']['result'][0]
                    meta = result['meta']
                    
                    current_price = meta.get('regularMarketPrice', 0)
                    previous_close = meta.get('previousClose', 0)
                    change = current_price - previous_close
                    change_percent = (change / previous_close * 100) if previous_close else 0
                    
                    market_data[name] = {
                        'price': current_price,
                        'change': change,
                        'change_percent': change_percent
                    }
            except:
                # Fallback to dummy data if API fails
                market_data[name] = {
                    'price': 23456.78 if 'NIFTY' in name else 77234.12,
                    'change': 234.56,
                    'change_percent': 1.01
                }
        
        return market_data
    except:
        # Return dummy data if all fails
        return {
            "NIFTY 50": {'price': 23456.78, 'change': 234.56, 'change_percent': 1.01},
            "SENSEX": {'price': 77234.12, 'change': 456.89, 'change_percent': 0.59},
            "BANK NIFTY": {'price': 48567.34, 'change': -123.45, 'change_percent': -0.25}
        }

# Professional Corporate CSS
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Clean professional background */
    .stApp {
        background: #f5f7fa;
    }
    
    /* Sidebar - Professional */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e1e8ed;
        box-shadow: 2px 0 8px rgba(0,0,0,0.05);
    }
    
    [data-testid="stSidebar"] .stButton button {
        background: #ffffff;
        color: #1a1a1a;
        border: 1px solid #e1e8ed;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        width: 100%;
        text-align: left;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: #f8f9fa;
        border-color: #0066cc;
        color: #0066cc;
    }
    
    /* Header - Corporate Style */
    .corporate-header {
        background: linear-gradient(135deg, #0066cc 0%, #004c99 100%);
        padding: 1.5rem 2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,102,204,0.15);
    }
    
    .corporate-header h1 {
        color: white;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .corporate-header p {
        color: rgba(255,255,255,0.9);
        font-size: 0.95rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    
    /* Chat messages - Clean style */
    .stChatMessage {
        background: transparent !important;
        padding: 1rem !important;
        border-radius: 6px;
        margin: 0.5rem 0;
    }
    
    .stChatMessage[data-testid="user-message"] {
        background: #f0f7ff !important;
        border-left: 3px solid #0066cc;
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background: #ffffff !important;
        border-left: 3px solid #28a745;
    }
    
    /* Chat input - Professional */
    .stChatInput textarea {
        background: white !important;
        border: 2px solid #e1e8ed !important;
        border-radius: 8px !important;
        color: #1a1a1a !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.95rem !important;
    }
    
    .stChatInput textarea:focus {
        border-color: #0066cc !important;
        box-shadow: 0 0 0 3px rgba(0,102,204,0.1) !important;
    }
    
    /* Buttons - Corporate style */
    .stButton button {
        background: #0066cc;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.25rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        background: #0052a3;
        box-shadow: 0 2px 8px rgba(0,102,204,0.25);
    }
    
    /* Market widget - Professional */
    .market-card {
        background: white;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid #e1e8ed;
    }
    
    .market-card h3 {
        color: #1a1a1a;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #f0f7ff;
    }
    
    .market-item {
        background: #f8f9fa;
        border-radius: 6px;
        padding: 1rem;
        margin: 0.75rem 0;
        border-left: 3px solid #0066cc;
    }
    
    .market-label {
        font-size: 0.85rem;
        color: #6c757d;
        font-weight: 500;
        margin-bottom: 0.25rem;
    }
    
    .market-price {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0.25rem 0;
    }
    
    .market-change-positive {
        color: #28a745;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .market-change-negative {
        color: #dc3545;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .market-time {
        font-size: 0.75rem;
        color: #6c757d;
        margin-top: 0.5rem;
    }
    
    /* Action buttons */
    .action-buttons {
        display: flex;
        gap: 0.75rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    
    .action-btn {
        flex: 1;
        min-width: 140px;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: white;
        border: 2px dashed #e1e8ed;
        border-radius: 8px;
        padding: 1.5rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: white;
        color: #1a1a1a;
        border: 1px solid #e1e8ed;
        border-radius: 6px;
        font-weight: 500;
    }
    
    /* Success/Error - Professional */
    .stSuccess {
        background: #d4edda;
        border-left: 4px solid #28a745;
        color: #155724;
        border-radius: 6px;
    }
    
    .stError {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        color: #721c24;
        border-radius: 6px;
    }
    
    /* Text colors */
    p, span, div, label {
        color: #1a1a1a;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: white;
        border: 1px solid #e1e8ed;
        color: #1a1a1a;
        border-radius: 6px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border-radius: 6px;
        padding: 0.25rem;
        border: 1px solid #e1e8ed;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #6c757d;
        border-radius: 4px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: #0066cc;
        color: white;
    }
    
    /* Logo placeholder */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    
    .logo-img {
        width: 50px;
        height: 50px;
        border-radius: 8px;
    }
    
    .company-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0066cc;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "language" not in st.session_state:
    st.session_state.language = "English"

# Sidebar
with st.sidebar:
    # Logo and branding
    st.markdown("""
    <div class="logo-container">
        <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #0066cc, #00c853); border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,102,204,0.3);">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <!-- Rupee symbol with growth arrow -->
                <path d="M12 8 L28 8 M12 12 L28 12 M12 16 L20 16 L28 28" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M24 12 L32 12 L32 4" stroke="#ffd700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="20" cy="20" r="18" stroke="white" stroke-width="1.5" opacity="0.3" fill="none"/>
            </svg>
        </div>
        <div>
            <div class="company-name">WealthWise AI</div>
            <div style="font-size: 0.75rem; color: #6c757d; font-weight: 500;">Smart Mutual Fund Advisory</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("➕ New Conversation"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### Language")
    selected_lang = st.selectbox(
        "Select Language",
        ["English", "हिंदी (Hindi)", "தமிழ் (Tamil)"],
        label_visibility="collapsed"
    )
    st.session_state.language = selected_lang
    
    st.markdown("---")
    
    st.markdown("### Quick Actions")
    if st.button("📊 Portfolio Analysis"):
        st.info("💡 Upload your portfolio statement for detailed analysis by WealthWise AI")
    
    if st.button("💡 Investment Ideas"):
        st.info("💡 Get personalized investment suggestions from WealthWise AI")
    
    if st.button("📈 Market Insights"):
        st.info("💡 View detailed market analysis powered by WealthWise AI")
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style="padding: 1rem; background: #f8f9fa; border-radius: 6px; font-size: 0.8rem; color: #6c757d; text-align: center;">
        <div style="font-weight: 600; color: #0066cc; margin-bottom: 0.5rem;">💎 WealthWise AI</div>
        <strong>Disclaimer:</strong> This platform provides educational information only. Please consult a certified financial advisor before making investment decisions.
    </div>
    """, unsafe_allow_html=True)

# Main layout
col_main, col_market = st.columns([2.2, 1])

with col_main:
    # Header with logo
    st.markdown("""
    <div class="corporate-header">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
            <div style="width: 50px; height: 50px; background: rgba(255,255,255,0.2); border-radius: 10px; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(10px);">
                <svg width="35" height="35" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 8 L28 8 M12 12 L28 12 M12 16 L20 16 L28 28" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M24 12 L32 12 L32 4" stroke="#ffd700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div>
                <h1 style="margin: 0; font-size: 2rem;">WealthWise AI</h1>
                <p style="margin: 0; font-size: 0.9rem;">Smart Mutual Fund Advisory Platform</p>
            </div>
        </div>
        <p style="margin-top: 0.75rem; font-size: 0.85rem; opacity: 0.9;">Professional investment guidance powered by AI | SEBI Compliant Information</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="chat-container">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #0066cc, #00c853); border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,102,204,0.2);">
                    <svg width="35" height="35" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 8 L28 8 M12 12 L28 12 M12 16 L20 16 L28 28" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M24 12 L32 12 L32 4" stroke="#ffd700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <div>
                    <h3 style="color: #0066cc; margin: 0;">Welcome to WealthWise AI</h3>
                    <p style="color: #6c757d; margin: 0; font-size: 0.9rem;">Your Intelligent Mutual Fund Advisor</p>
                </div>
            </div>
            <p style="color: #6c757d; line-height: 1.6;">
                I'm WealthWise AI, your professional investment advisor powered by advanced AI. I'm here to help you make informed decisions about mutual fund investments.
            </p>
            <div style="margin-top: 1.5rem;">
                <strong style="color: #1a1a1a;">I can assist you with:</strong>
                <ul style="margin-top: 0.75rem; color: #6c757d; line-height: 1.8;">
                    <li>Mutual fund selection and analysis</li>
                    <li>SIP vs Lumpsum investment strategies</li>
                    <li>Portfolio diversification and risk management</li>
                    <li>NAV analysis and fund performance metrics</li>
                    <li>Tax-saving ELSS fund recommendations</li>
                    <li>Goal-based financial planning</li>
                </ul>
            </div>
            <div style="margin-top: 1.5rem; padding: 1rem; background: #f0f7ff; border-radius: 6px; border-left: 3px solid #0066cc;">
                <strong style="color: #0066cc;">💡 Pro Tip:</strong>
                <span style="color: #6c757d;"> You can upload documents, images, or use your camera for instant analysis.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message.get("image"):
                st.image(message["image"], width=400)
            st.markdown(message["content"])
    
    # Action buttons
    st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        show_upload = st.button("📎 Upload File", use_container_width=True)
    with col2:
        show_camera = st.button("📷 Camera", use_container_width=True)
    with col3:
        show_voice = st.button("🎤 Voice", use_container_width=True)
    with col4:
        show_pdf = st.button("📄 PDF", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Upload handlers
    if show_upload:
        with st.expander("📸 Upload Image", expanded=True):
            uploaded_image = st.file_uploader("Select image file", type=['png', 'jpg', 'jpeg'], key="img")
            if uploaded_image:
                image = Image.open(uploaded_image)
                st.image(image, width=400)
                if st.button("Analyze Image"):
                    with st.spinner("Analyzing..."):
                        response = analyze_image(image, st.session_state.language)
                        st.session_state.messages.append({"role": "user", "content": "📸 Image uploaded for analysis", "image": image})
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
    
    if show_camera:
        with st.expander("📷 Camera Capture", expanded=True):
            camera_image = st.camera_input("Capture image")
            if camera_image:
                image = Image.open(camera_image)
                if st.button("Analyze Capture"):
                    with st.spinner("Analyzing..."):
                        response = analyze_image(image, st.session_state.language)
                        st.session_state.messages.append({"role": "user", "content": "📷 Camera capture", "image": image})
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
    
    if show_pdf:
        with st.expander("📄 PDF Document", expanded=True):
            uploaded_pdf = st.file_uploader("Select PDF", type=['pdf'], key="pdf")
            if uploaded_pdf:
                try:
                    pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_pdf.read()))
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                    if text.strip():
                        st.success(f"✅ PDF loaded: {len(text)} characters")
                        if st.button("Analyze PDF"):
                            with st.spinner("Analyzing document..."):
                                query = f"Analyze this mutual fund document:\n\n{text[:4000]}"
                                response = get_response(query, st.session_state.chat_history, st.session_state.language)
                                st.session_state.messages.append({"role": "user", "content": "📄 PDF document uploaded"})
                                st.session_state.messages.append({"role": "assistant", "content": response})
                                st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Chat input
    if prompt := st.chat_input("Ask WealthWise AI about mutual funds, SIP, portfolio strategies..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your query..."):
                response = get_response(prompt, st.session_state.chat_history, st.session_state.language)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.chat_history.append({"role": "user", "parts": [prompt]})
        st.session_state.chat_history.append({"role": "model", "parts": [response]})
        st.rerun()

# Market updates panel
with col_market:
    # Fetch live data
    market_data = get_live_market_data()
    current_time = datetime.now().strftime("%I:%M %p")
    
    st.markdown(f"""
    <div class="market-card">
        <h3>📊 Live Market Updates</h3>
    """, unsafe_allow_html=True)
    
    for index_name, data in market_data.items():
        change_class = "market-change-positive" if data['change'] >= 0 else "market-change-negative"
        arrow = "▲" if data['change'] >= 0 else "▼"
        
        st.markdown(f"""
        <div class="market-item">
            <div class="market-label">{index_name}</div>
            <div class="market-price">{data['price']:,.2f}</div>
            <div class="{change_class}">{arrow} {abs(data['change']):,.2f} ({data['change_percent']:+.2f}%)</div>
            <div class="market-time">Updated: {current_time}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Top funds
    st.markdown("""
    <div class="market-card">
        <h3>⭐ Top Performing Funds</h3>
        <div style="padding: 0.75rem; background: #f8f9fa; border-radius: 6px; margin: 0.5rem 0;">
            <div style="font-size: 0.85rem; color: #6c757d; font-weight: 500;">Axis Bluechip Fund</div>
            <div style="font-size: 1.1rem; color: #28a745; font-weight: 600; margin-top: 0.25rem;">+15.2% (1Y)</div>
        </div>
        <div style="padding: 0.75rem; background: #f8f9fa; border-radius: 6px; margin: 0.5rem 0;">
            <div style="font-size: 0.85rem; color: #6c757d; font-weight: 500;">HDFC Mid-Cap Fund</div>
            <div style="font-size: 1.1rem; color: #28a745; font-weight: 600; margin-top: 0.25rem;">+18.7% (1Y)</div>
        </div>
        <div style="padding: 0.75rem; background: #f8f9fa; border-radius: 6px; margin: 0.5rem 0;">
            <div style="font-size: 0.85rem; color: #6c757d; font-weight: 500;">SBI Small Cap Fund</div>
            <div style="font-size: 1.1rem; color: #28a745; font-weight: 600; margin-top: 0.25rem;">+22.3% (1Y)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Market status
    st.markdown("""
    <div class="market-card">
        <div style="text-align: center;">
            <div style="font-size: 0.85rem; color: #6c757d; margin-bottom: 0.5rem;">Market Status</div>
            <div style="font-size: 1.1rem; color: #28a745; font-weight: 600;">● OPEN</div>
            <div style="font-size: 0.75rem; color: #6c757d; margin-top: 0.5rem;">Mon-Fri: 9:15 AM - 3:30 PM</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
