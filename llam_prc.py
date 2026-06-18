import warnings
# Suppress the DeprecationWarning from langchain_community
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.chat_models import ChatLlamaCpp
from langchain_core.messages import HumanMessage, SystemMessage

# Use the exact absolute path to your model file
MODEL_PATH = "/home/ubuntu/models/Qwen2.5-14B-Instruct-Q4_K_M.gguf"

# Initialize the model
llm = ChatLlamaCpp(
    model_path=MODEL_PATH,
    temperature=0.7,
    max_tokens=512,
    n_ctx=2048,
    n_gpu_layers=0,  # Set to -1 if you want to offload to an NVIDIA GPU
    verbose=False,
)

# Structuring messages for the Qwen Instruct model
messages = [
    SystemMessage(content="You are a helpful, clear, and concise AI assistant."),
    HumanMessage(content="Explain the difference between a physical server and a cloud server in two sentences.")
]

print("Sending request to Qwen2.5-14B...")

# Invoke and print response
response = llm.invoke(messages)

print("\n--- Model Response ---")
print(response.content)
