import streamlit as st
import requests
from tools import get_currency, get_exchange_rate, get_stock_index, get_map

st.set_page_config(page_title="Currency & Stock MCP Agent", layout="wide")

# ---------------------- CUSTOM UI ----------------------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }

    .main-title {
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 15px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='main-title'>💱 Currency & Stock Market MCP Agent</div>", unsafe_allow_html=True)

st.write("Get official currency, exchange rates, stock index value, and exchange location.")

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

country = st.text_input("Enter country (Japan / India / US / UK / China / South Korea)")

# ---------------------- MAIN LOGIC ----------------------

if st.button("Get Details"):

    if country:

        with st.spinner("Running MCP multi-tool reasoning..."):

            currency_result = get_currency(country)

            currency_code = currency_result.split(":")[-1].strip()

            exchange_result = get_exchange_rate(currency_code)

            stock_result = get_stock_index(country)

            exchange_location = get_map(country)

            combined_context = f"""
            {currency_result}
            {exchange_result}
            {stock_result}
            Stock Exchange Location: {exchange_location}
            """

            url = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }

            prompt = f"""
            Using the following real-time financial data:

            {combined_context}

            Format nicely with headings:
            Official Currency
            Exchange Rates
            Major Stock Exchange
            Current Index Value
            """

            data = {
                "model": "meta-llama/llama-3-8b-instruct",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

            response = requests.post(url, headers=headers, json=data)
            result = response.json()

            if response.status_code == 200:
                final_output = result["choices"][0]["message"]["content"]
            else:
                final_output = f"Error: {response.status_code}"

        # ---------------------- DISPLAY ----------------------

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown(final_output)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>📍 Stock Exchange Location</div>", unsafe_allow_html=True)

        st.components.v1.iframe(
            f"https://www.google.com/maps?q={exchange_location}&output=embed",
            height=400
        )

    else:
        st.warning("Please enter a country.")
