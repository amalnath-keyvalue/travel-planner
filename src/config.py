import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    AGENT_MODEL = os.getenv("AGENT_MODEL", "llama3-70b-8192")
    AGENT_TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.1"))

    @classmethod
    def get_llm(cls):
        if cls.GROQ_API_KEY:
            return ChatGroq(
                groq_api_key=cls.GROQ_API_KEY,
                model_name=cls.AGENT_MODEL,
                temperature=cls.AGENT_TEMPERATURE,
            )
        raise ValueError("GROQ_API_KEY not found in environment variables")
