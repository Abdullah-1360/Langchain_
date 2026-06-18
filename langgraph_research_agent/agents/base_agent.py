"""Base agent class for all research agents"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from langchain_openai import ChatOpenAI
from config.settings import LLM_MODEL, LLM_TEMPERATURE


def _get_llm():
    """Get LLM from local API server (Qwen2.5-1.5B-Instruct-Q4_K_)"""
    # Using local API server running on localhost:8080
    # This matches the setup used in jsonoutputparser.py
    print("🚀 Connecting to local Qwen2.5-1.5B model server...")
    
    llm = ChatOpenAI(
        base_url="http://127.0.0.1:8080/v1",
        api_key="not-needed",
        model="Qwen2.5-1.5B-Instruct-Q4_K_M",
        temperature=LLM_TEMPERATURE,
        max_tokens=2048,
    )
    print("✅ Connected to local model successfully!")
    return llm


class BaseAgent(ABC):
    """Base class for all research agents"""
    
    def __init__(self, name: str):
        """Initialize the base agent"""
        self.name = name
        self.llm = _get_llm()
    
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's logic"""
        pass
    
    def __call__(self, *args, **kwargs) -> Dict[str, Any]:
        """Allow the agent to be called directly"""
        return self.execute(*args, **kwargs)

