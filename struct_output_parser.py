import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser,StrOutputParser

load_dotenv()

# Same model setup as output_parsing.py
API_URL = "http://127.0.0.1:8080/v1"

model = ChatOpenAI(
    base_url=API_URL,
    api_key="not-needed",
    model="Qwen2.5-3B-Instruct-Q4_K_M",
    max_tokens=2048,
    temperature=0,
)

print("=== PydanticOutputParser Example ===\n")

# Step 1: Define the data schema using Pydantic
class Sentiment(BaseModel):
    text: str = Field(description="The input text")
    sentiment: str = Field(description="POSITIVE, NEGATIVE, or NEUTRAL")
    confidence: float = Field(description="Confidence score 0-1")

# Step 2: Initialize PydanticOutputParser
parser = PydanticOutputParser(pydantic_object=Sentiment)

# Step 3: Create prompt with format instructions
prompt = ChatPromptTemplate.from_messages([
    ("system", "Analyze the sentiment of the text. {format_instructions}"),
    ("user", "{text}")
])

# Add parser format instructions to prompt
prompt = prompt.partial(format_instructions=parser.get_format_instructions())

# Step 4: Build chain
chain = prompt | model | parser

# Step 5: Invoke
result = chain.invoke({"text": "I love this product! It's amazing!"})

print(f"Result: {result}")
print(f"Type: {type(result)}")
print(f"Sentiment: {result.sentiment}")
print(f"Confidence: {result.confidence}")
