import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Same model setup as output_parsing.py
API_URL = "http://127.0.0.1:8080/v1"

model = ChatOpenAI(
    base_url=API_URL,
    api_key="not-needed",
    model="Qwen3-8B-Q6_K",
    max_tokens=2048,
    temperature=0.1,
)

# Initialize the StrOutputParser
str_parser = StrOutputParser()

# Example 1: Simple String Output
print("=== Example 1: Simple Product Review Summary ===")
messages_1 = [
    SystemMessage(content="You are a concise product review summarizer. Provide a brief 1-2 sentence summary."),
    HumanMessage(content="The Samsung Galaxy S25 Ultra is excellent but expensive. Great display and camera, but similar design to S24.")
]

result_1 = model.invoke(messages_1)
parsed_result_1 = str_parser.invoke(result_1)
print(parsed_result_1)
print(f"Type: {type(parsed_result_1)}\n")

# Example 2: Using LLMChain with prompt template and parser
print("=== Example 2: Using Prompt Template with StrOutputParser ===")
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that extracts sentiment from text. Reply with only: POSITIVE, NEGATIVE, or NEUTRAL"),
    ("user", "{text}")
])

chain = prompt_template | model | str_parser

sentiment_text = "This product exceeded all my expectations! Absolutely love it."
result_2 = chain.invoke({"text": sentiment_text})
print(f"Sentiment: {result_2}\n")

# Example 3: Processing Multiple Inputs
print("=== Example 3: Batch Processing ===")
reviews = [
    "Amazing quality and fast shipping!",
    "Terrible experience, never buying again",
    "It's okay, nothing special"
]

sentiment_chain = prompt_template | model | str_parser

for review in reviews:
    sentiment = sentiment_chain.invoke({"text": review})
    print(f"Review: {review}")
    print(f"Sentiment: {sentiment}\n")
