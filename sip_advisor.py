# ---- Imports ----
import os
from dotenv import load_dotenv
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import openai
from openai import RateLimitError

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Your question here"}
        ]
    )
    st.write(response.choices[0].message.content)
except RateLimitError:
    st.error("Rate limit exceeded. Please wait and try again later.")


load_dotenv()

# ---- OpenAI Setup ----
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---- Title ----
st.title("📈 SIP Investment + AI Advisor")

# ---- User Inputs ----
sip = st.number_input("Monthly SIP Amount (₹)", min_value=100, step=100, value=5000)
years = st.number_input("Investment Duration (Years)", min_value=1, max_value=40, value=20)
annual_rate = st.number_input("Expected Annual Return (%)", min_value=1.0, max_value=20.0, value=12.0)

# ---- Calculations ----
months = years * 12
monthly_rate = annual_rate / 12 / 100
future_value = sip * (((1 + monthly_rate)**months - 1) * (1 + monthly_rate)) / monthly_rate
total_invested = sip * months
returns = future_value - total_invested

# ---- Results ----
st.subheader("📊 Results")
st.write(f"**Total Invested**: ₹{int(total_invested):,}")
st.write(f"**Estimated Returns**: ₹{int(returns):,}")
st.write(f"**Final Value**: ₹{int(future_value):,}")

# ---- Graph ----
values = [sip * i for i in range(1, months + 1)]
future_vals = [sip * (((1 + monthly_rate)**i - 1) * (1 + monthly_rate)) / monthly_rate for i in range(1, months + 1)]

plt.plot(range(1, months+1), future_vals, label='Future Value')
plt.xlabel("Month")
plt.ylabel("Amount (₹)")
plt.title("SIP Growth Over Time")
plt.legend()
st.pyplot(plt)

# ---- AI Financial Advisor ----
prompt = f"""
My SIP is ₹{sip} per month for {years} years with an expected annual return of {annual_rate}%.

Based on this, what advice would you give me as an AI financial advisor? Please mention:
- If the SIP amount is sufficient for long-term goals
- How it compares to inflation
- Tips to improve my portfolio
"""

if st.button("💡 Get AI Investment Advice"):
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional financial advisor."},
                {"role": "user", "content": prompt}
            ]
        )
        advice = response.choices[0].message.content
        st.markdown("### 💬 AI Financial Advice")
        st.write(advice)
