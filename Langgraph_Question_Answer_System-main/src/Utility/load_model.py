from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv
load_dotenv()
from config import Settings
from functools import lru_cache

@lru_cache
def get_model():
    llm = ChatGroq(
        model= Settings().LLM,
        temperature=Settings().TEMPERATURE
    )
    return llm 
