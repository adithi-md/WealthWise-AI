# 🚀 Quick Start Guide

## Get Started in 5 Minutes!

### 1️⃣ Install Dependencies
```bash
pip install streamlit google-generativeai python-dotenv PyPDF2 Pillow
```

### 2️⃣ Set API Key
Create `.env` file:
```
GEMINI_API_KEY=your_key_here
```

Get your key: https://makersuite.google.com/app/apikey

### 3️⃣ Run the App
```bash
# Standard version
streamlit run app.py

# Enhanced version (Recommended)
streamlit run app_enhanced.py
```

### 4️⃣ Access the App
Open browser: http://localhost:8501

## 🎯 Try These Features

### Text Chat
Just type: "What is SIP?"

### Upload Image
1. Click "📸 Upload Image"
2. Select a chart/graph
3. Click "Analyze"

### Upload PDF
1. Click "📄 Upload PDF"
2. Select mutual fund document
3. Click "Analyze"

### Use Camera
1. Click "📷 Use Camera"
2. Allow camera access
3. Capture photo
4. Click "Analyze"

### Change Language
1. Open sidebar
2. Select: English / हिंदी / தமிழ்
3. Chat in your language!

## 🌐 Multilingual Examples

**English:**
```
"Explain mutual funds"
```

**Hindi:**
```
"म्यूचुअल फंड क्या है?"
```

**Tamil:**
```
"மியூச்சுவல் ஃபண்ட் என்றால் என்ன?"
```

## 🎨 Two Versions Available

### app.py (Standard)
- Clean interface
- All features
- Light theme option

### app_enhanced.py (Premium) ⭐
- ChatGPT-style dark theme
- Gradient design
- Premium animations
- **Recommended for best experience**

## 🆘 Troubleshooting

**Error: Module not found**
```bash
pip install -r requirements.txt
```

**Error: Invalid API key**
- Check `.env` file
- Verify key from Google AI Studio

**Camera not working**
- Allow browser camera permissions
- Use HTTPS or localhost

**PDF not loading**
- Check file size (< 10MB recommended)
- Ensure it's a valid PDF

## 📱 Mobile Access

1. Find your network IP:
```bash
ipconfig  # Windows
ifconfig  # Mac/Linux
```

2. Access from phone:
```
http://YOUR_IP:8501
```

## 🎉 You're Ready!

Start chatting with your AI Mutual Fund Advisor!

---

**Need Help?** Check README.md for detailed documentation.
