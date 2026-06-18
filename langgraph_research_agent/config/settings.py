"""Settings and configuration for the research agent"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration - Support for Local Models
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "local")  # "local" or "openai"
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5-1.5b")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))

# Local Model Configuration (for llama-cpp-python)
LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH", "./models/qwen2.5-1.5b-instruct-q4_k.gguf")
N_GPU_LAYERS = int(os.getenv("N_GPU_LAYERS", "50"))  # Set to -1 for GPU acceleration, 0 for CPU
N_THREADS = int(os.getenv("N_THREADS", "4"))
CONTEXT_WINDOW = int(os.getenv("CONTEXT_WINDOW", "2048"))

# OpenAI Configuration (fallback)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Agent Configuration
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "10"))
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "60"))

# Search Configuration
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

