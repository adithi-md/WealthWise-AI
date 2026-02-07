import streamlit as st
from chatbot import get_response

st.set_page_config(page_title="Personalized Investment Chatbot")

st.title("📊 Personalized Investment Chatbot")

age = st.sidebar.number_input("Age", 18, 60, 18)
goal = st.sidebar.selectbox("Goal", ["Education", "Wealth", "Retirement"])
risk = st.sidebar.selectbox("Risk Appetite", ["Low", "Medium", "High"])

user_input = st.text_input("Ask your investment question")

if user_input:
    user_profile = {
        "age": age,
        "goal": goal,
        "risk": risk
    }
    response = get_response(user_input, user_profile)
    st.success(response)

st.caption("📌 Educational purpose only.")
