# import warnings
# # Suppress the DeprecationWarning from langchain_community
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# from langchain_community.chat_models import ChatLlamaCpp
# from langchain_core.messages import HumanMessage, SystemMessage

# MODEL_PATH = "/home/ubuntu/models/Qwen2.5-14B-Instruct-Q4_K_M.gguf"

# # 1. Define your style profiles with specific system instructions and temperatures
# STYLE_PROFILES = {
#     "1": {
#         "name": "Code-Oriented",
#         "system": "You are an expert software engineer. Provide highly technical, clean, and optimized code solutions with brief, accurate architectural explanations. Skip conversational fluff.",
#         "temperature": 0.1  # Low temperature for deterministic, structured code
#     },
#     "2": {
#         "name": "Playful",
#         "system": "You are a witty, enthusiastic, and highly energetic AI sidekick. Use light humor, fun analogies, and a vibrant, conversational tone to explain concepts.",
#         "temperature": 0.85 # Higher temperature for more creative/unexpected responses
#     },
#     "3": {
#         "name": "Thoughtful & Analytical",
#         "system": "You are a deep-thinking philosopher and rigorous research analyst. Break down concepts from multiple perspectives, address underlying nuances, and provide structural depth.",
#         "temperature": 0.5  # Balanced temperature for balanced reasoning
#     },
#     "4": {
#         "name": "Default (Concise Assistant)",
#         "system": "You are a helpful, clear, and concise AI assistant.",
#         "temperature": 0.7
#     }
# }

# print("Initializing Qwen2.5-14B Base Model...")
# # Initialize the baseline model config
# llm = ChatLlamaCpp(
#     model_path=MODEL_PATH,
#     max_tokens=1024, # Increased token budget for detailed/code responses
#     n_ctx=4096,      # Expanded context window for deep thought/larger snippets
#     n_gpu_layers=0,
#     verbose=False,
# )

# print("Model ready!")

# while True:
#     print("\n" + "="*60)
#     print("AVAILABLE STYLES:")
#     for key, profile in STYLE_PROFILES.items():
#         print(f" [{key}] {profile['name']}")
    
#     style_choice = input("\nSelect a style number (or type 'exit' to quit): ").strip()
    
#     if style_choice.lower() in ['exit', 'quit', 'q']:
#         print("Goodbye!")
#         break
        
#     # Fallback to default if choice is invalid
#     selected_style = STYLE_PROFILES.get(style_choice, STYLE_PROFILES["4"])
#     print(f"\n>> Active Style: {selected_style['name']} (Temp: {selected_style['temperature']})")
    
#     user_query = input("Enter your prompt: ").strip()
#     if not user_query:
#         print("Prompt cannot be empty.")
#         continue

#     # 2. Dynamic Parameters: Override the temperature at invocation time
#     # This alters the generation behavior alongside the text prompt
#     messages = [
#         SystemMessage(content=selected_style["system"]),
#         HumanMessage(content=user_query)
#     ]

#     print("\nThinking...")
#     try:
#         # LangChain allows passing runtime configurations via config dictionary
#         response = llm.invoke(messages, config={"temperature": selected_style["temperature"]})
#         print("\n--- Response ---")
#         print(response.content)
#     except Exception as e:
#         print(f"\nAn error occurred: {e}")



import warnings
# Suppress DeprecationWarnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Since llama-server is running on port 8085, we connect to it locally.
# We don't need a model path anymore; the server handles the model file.
API_URL = "http://127.0.0.1:8080/v1"

# Define style profiles with specific system instructions and temperatures
STYLE_PROFILES = {
    "1": {
        "name": "Code-Oriented",
        "system": "You are an expert software engineer. Provide highly technical, clean, and optimized code solutions with brief, accurate architectural explanations. Skip conversational fluff.",
        "temperature": 0.1  
    },
    "2": {
        "name": "Playful",
        "system": "You are a witty, enthusiastic, and highly energetic AI sidekick. Use light humor, fun analogies, and a vibrant, conversational tone to explain concepts.",
        "temperature": 0.85 
    },
    "3": {
        "name": "Thoughtful & Analytical",
        "system": "You are a deep-thinking philosopher and rigorous research analyst. Break down concepts from multiple perspectives, address underlying nuances, and provide structural depth.",
        "temperature": 0.5  
    },
    "4": {
        "name": "Default (Concise Assistant)",
        "system": "You are a helpful, clear, and concise AI assistant.",
        "temperature": 0.7
    }
}

print("Connecting to Gemma-4-26B (via llama-server)...")

# Initialize the client pointing to your active llama-server instance.
# We pass a dummy api_key because llama-server doesn't require one by default.
llm = ChatOpenAI(
    base_url=API_URL,
    api_key="not-needed",
    model="Qwen3-8B-Q6_K", # Updated matching your currently active background model
    max_tokens=1024,
)

print("Server connection established!")

while True:
    print("\n" + "="*60)
    print("AVAILABLE STYLES:")
    for key, profile in STYLE_PROFILES.items():
        print(f" [{key}] {profile['name']}")
    
    style_choice = input("\nSelect a style number (or type 'exit' to quit): ").strip()
    
    if style_choice.lower() in ['exit', 'quit', 'q']:
        print("Goodbye!")
        break
        
    # Fallback to default if choice is invalid
    selected_style = STYLE_PROFILES.get(style_choice, STYLE_PROFILES["4"])
    print(f"\n>> Active Style: {selected_style['name']} (Temp: {selected_style['temperature']})")
    
    user_query = input("Enter your prompt: ").strip()
    if not user_query:
        print("Prompt cannot be empty.")
        continue

    messages = [
        SystemMessage(content=selected_style["system"]),
        HumanMessage(content=user_query)
    ]

    print("\nThinking...")
    try:
        # Pass the dynamic temperature straight to the invoke call
        response = llm.invoke(messages, temperature=selected_style["temperature"])
        print("\n--- Response ---")
        print(response.content)
    except Exception as e:
        print(f"\nAn error occurred: {e}")