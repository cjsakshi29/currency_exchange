import streamlit as st
import requests
from tools import get_currency, get_exchange_rate, get_stock_index, get_map

st.set_page_config(page_title="Currency & Stock MCP Agent", layout="wide")

st.title("💱 Currency & Stock Market MCP Agent")

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

country = st.text_input("Enter country (Japan / India / US / UK / China / South Korea)")

if st.button("Get Details"):

    if country:

        with st.spinner("Running MCP multi-tool reasoning..."):

            # -------- TOOL EXECUTION (MCP) --------
            currency_result = get_currency(country)

            # Extract currency code
            currency_code = currency_result.split(":")[-1].strip()

            exchange_result = get_exchange_rate(currency_code)

            stock_result = get_stock_index(country)

            exchange_location = get_map(country)

            # -------- CONTEXT AGGREGATION --------
            combined_context = f"""
            {currency_result}

            {exchange_result}

            {stock_result}

            Stock Exchange Location: {exchange_location}
            """

            # -------- LLM REASONING --------
            url = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }

            prompt = f"""
            Using the following real-time financial data:

            {combined_context}

            Format the output clearly with:
            - Official Currency
            - Exchange Rates
            - Major Stock Exchange
            - Current Index Value
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

        st.markdown(final_output)

        st.subheader("📍 Stock Exchange Location")
        st.components.v1.iframe(
            f"https://www.google.com/maps?q={exchange_location}&output=embed",
            height=400
        )

    else:
        st.warning("Please enter a country.")
