import os
from langchain_groq import ChatGroq # Changed from langchain_openai
from tavily import TavilyClient

def get_llm() -> ChatGroq:
    return ChatGroq(
        # Llama 3.3 70B is very similar to GPT-4o-mini in reasoning speed
        model="llama-3.3-70b-versatile", 
        temperature=0.2,
        groq_api_key=os.getenv("GROQ_API_KEY"), # Make sure this matches your .env
    )

def get_tavily_client() -> TavilyClient:
    return TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
