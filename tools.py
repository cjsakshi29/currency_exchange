import yfinance as yf
import requests
import streamlit as st

# ---------------- CURRENCY TOOL ----------------
def get_currency(country):

    currency_map = {
        "japan": "JPY",
        "india": "INR",
        "us": "USD",
        "uk": "GBP",
        "china": "CNY",
        "south korea": "KRW"
    }

    country = country.lower()

    if country in currency_map:
        return f"Official Currency of {country.title()}: {currency_map[country]}"
    else:
        return "Currency data not available."


# ---------------- EXCHANGE RATE TOOL ----------------
def get_exchange_rate(currency):

    API_KEY = st.secrets["EXCHANGE_API_KEY"]

    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{currency}"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        rates = data["conversion_rates"]

        return f"""
1 {currency} equals:
USD: {rates['USD']}
INR: {rates['INR']}
GBP: {rates['GBP']}
EUR: {rates['EUR']}
"""
    else:
        return "Exchange rate data not available."


# ---------------- STOCK INDEX TOOL ----------------
def get_stock_index(country):

    index_map = {
        "japan": "^N225",
        "india": "^BSESN",
        "us": "^GSPC",
        "uk": "^FTSE",
        "china": "000001.SS",
        "south korea": "^KS11"
    }

    country = country.lower()

    if country in index_map:
        ticker = yf.Ticker(index_map[country])
        data = ticker.history(period="1d")

        if not data.empty:
            price = data["Close"][0]
            return f"Current Index Value: {price}"
        else:
            return "Index data unavailable."
    else:
        return "Stock index not found."


# ---------------- GOOGLE MAP TOOL ----------------
def get_map(country):

    exchange_map = {
        "japan": "Tokyo Stock Exchange",
        "india": "Bombay Stock Exchange",
        "us": "New York Stock Exchange",
        "uk": "London Stock Exchange",
        "china": "Shanghai Stock Exchange",
        "south korea": "Korea Exchange"
    }

    country = country.lower()

    if country in exchange_map:
        place = exchange_map[country]
        return place
    else:
        return "Exchange location not found."
