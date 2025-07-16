import streamlit as st
from utils.helpers import add_expense, set_income, get_summary, load_data
import google.generativeai as genai
import os

# Load Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("Please set your GEMINI_API_KEY as an environment variable.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# UI Layout
st.set_page_config(page_title="💰 Budget Assistant", layout="centered")
st.title("💰 Personal Budgeting Assistant")

# Income Section
st.header("📥 Set Monthly Income")
income = st.number_input("Monthly Income ($)", min_value=0.0, step=100.0)
if st.button("💾 Save Income"):
    set_income(income)
    st.success("Income saved successfully!")

# Expense Entry
st.header("📤 Add Expense")
amount = st.number_input("Expense Amount ($)", min_value=0.0, step=10.0)
category = st.selectbox("Category", ["Food", "Transport", "Rent", "Entertainment", "Other"])
description = st.text_input("Description")
if st.button("➕ Add Expense"):
    add_expense(amount, category, description)
    st.success("Expense added!")

# Summary Section
st.header("📊 Monthly Summary")
summary = get_summary()
st.write(f"**Income:** ${summary['income']}")
st.write(f"**Total Expenses:** ${summary['total_expense']}")
st.write(f"**Remaining Balance:** ${summary['remaining']}")

if summary["overspending"]:
    st.error("⚠️ You are overspending this month!")

# Gemini Assistant
st.header("💬 Ask the Budget Assistant")
user_query = st.text_area("Ask a question (e.g., how to save money, control spending...)")
if st.button("Ask Gemini"):
    data = load_data()
    prompt = f"""I have a monthly income of ${data['income']} and these expenses: {data['expenses']}.
    {user_query}"""
    with st.spinner("Gemini is thinking..."):
        gemini_response = chat_with_gemini(prompt)
    st.markdown(f"**Gemini says:** {gemini_response}")
