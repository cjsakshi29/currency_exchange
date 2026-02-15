import streamlit as st
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
import streamlit as st
from tools import get_currency, get_exchange_rate, get_stock_index, get_map

st.set_page_config(page_title="Currency & Stock Agent", layout="wide")

st.title("💱 Currency & Stock Market MCP Agent")

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

llm = ChatOpenAI(
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="meta-llama/llama-3-8b-instruct",
    temperature=0.7
)

tools = [
    Tool(name="Currency Tool", func=get_currency, description="Get official currency of country"),
    Tool(name="Exchange Tool", func=get_exchange_rate, description="Get exchange rate details"),
    Tool(name="Stock Tool", func=get_stock_index, description="Get stock index value"),
    Tool(name="Map Tool", func=get_map, description="Get stock exchange location")
]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

country = st.text_input("Enter country name")

if st.button("Get Details"):

    if country:

        result = agent.run(
            f"""
            Provide:
            1. Official currency of {country}
            2. Real-time exchange rate of that currency to USD, INR, GBP, EUR
            3. Major stock exchange and its index current value
            """
        )

        st.markdown(result)

        exchange_name = get_map(country)
        st.subheader("📍 Stock Exchange Location")
        st.components.v1.iframe(
            f"https://www.google.com/maps?q={exchange_name}&output=embed",
            height=400
        )

    else:
        st.warning("Enter country name.")
