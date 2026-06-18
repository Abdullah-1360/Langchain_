import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import json

load_dotenv()

# Same model setup as output_parsing.py
API_URL = "http://127.0.0.1:8080/v1"

model = ChatOpenAI(
    base_url=API_URL,
    api_key="not-needed",
    model="Qwen2.5-1.5B-Instruct-Q4_K_M",
    max_tokens=2048,
    temperature=0,
)

# ==================== Example 1: Basic JSON Parser ====================
print("=== Example 1: Basic JSON Extraction ===\n")

# Define the JSON schema using Pydantic
class ProductInfo(BaseModel):
    name: str = Field(description="Product name")
    rating: float = Field(description="Product rating out of 5")
    price: str = Field(description="Product price")
    in_stock: bool = Field(description="Whether product is in stock")

# Initialize JSON parser
json_parser = JsonOutputParser(pydantic_object=ProductInfo)

# Create prompt that tells the model to output JSON
prompt_1 = ChatPromptTemplate.from_messages([
    ("system", "Extract product information and return as JSON. {format_instructions}"),
    ("user", "{product_text}")
])

# Partial format the prompt with schema instructions
prompt_1 = prompt_1.partial(format_instructions=json_parser.get_format_instructions())

# Build chain and convert dict to Pydantic model
chain_1 = prompt_1 | model | json_parser | (lambda x: ProductInfo(**x))

product_text = """
Samsung Galaxy S25 Ultra - 4.8 stars rating, priced at $1,299, currently available in stock
"""

result_1 = chain_1.invoke({"product_text": product_text})
print(f"Parsed Result: {result_1}")
print(f"Type: {type(result_1)}")
print(f"Name: {result_1.name}, Rating: {result_1.rating}, Price: {result_1.price}\n")

# ==================== Example 2: Complex Nested JSON ====================
print("=== Example 2: Complex Nested JSON Structure ===\n")

class ReviewDetails(BaseModel):
    pros: list[str] = Field(description="List of positive points")
    cons: list[str] = Field(description="List of negative points")
    overall_sentiment: str = Field(description="POSITIVE, NEGATIVE, or NEUTRAL")

class ProductReview(BaseModel):
    product: str = Field(description="Product name")
    reviewer: str = Field(description="Reviewer name")
    details: ReviewDetails = Field(description="Review details")

json_parser_2 = JsonOutputParser(pydantic_object=ProductReview)

prompt_2 = ChatPromptTemplate.from_messages([
    ("system", "Parse the review and extract structured data. Return valid JSON. {format_instructions}"),
    ("user", "{review_text}")
])

prompt_2 = prompt_2.partial(format_instructions=json_parser_2.get_format_instructions())
chain_2 = prompt_2 | model | json_parser_2 | (lambda x: ProductReview(**x))

review_text = """
Product: iPhone 15 Pro
Reviewer: John Smith
Review: The camera quality is excellent and the battery lasts all day. The price is quite high, 
and it doesn't come with a charger. Overall, I'm satisfied with this purchase.
"""

result_2 = chain_2.invoke({"review_text": review_text})
print(f"Parsed Review: {result_2}")
print(f"Product: {result_2.product}")
print(f"Reviewer: {result_2.reviewer}")
print(f"Sentiment: {result_2.details.overall_sentiment}")
print(f"Pros: {result_2.details.pros}\n")

# ==================== Example 3: Batch Processing ====================
print("=== Example 3: Batch Processing Multiple Reviews ===\n")

reviews = [
    "Product: Laptop X, Great performance but expensive",
    "Product: Monitor Z, Perfect display quality, affordable price",
    "Product: Keyboard M, Comfortable typing experience, good durability"
]

class SimpleReview(BaseModel):
    product: str = Field(description="Product name")
    summary: str = Field(description="Brief review summary")

json_parser_3 = JsonOutputParser(pydantic_object=SimpleReview)

prompt_3 = ChatPromptTemplate.from_messages([
    ("system", "Extract product and summary. {format_instructions}"),
    ("user", "{review}")
])

prompt_3 = prompt_3.partial(format_instructions=json_parser_3.get_format_instructions())
chain_3 = prompt_3 | model | json_parser_3 | (lambda x: SimpleReview(**x))

for review in reviews:
    result = chain_3.invoke({"review": review})
    print(f"Product: {result.product}")
    print(f"Summary: {result.summary}")
    print("---")

# ==================== Example 4: Raw JSON Output ====================
print("\n=== Example 4: Raw JSON Output (no schema) ===\n")

# JsonOutputParser without Pydantic model for flexible JSON
json_parser_4 = JsonOutputParser()

prompt_4 = ChatPromptTemplate.from_messages([
    ("system", "Return a valid JSON object with product stats"),
    ("user", "Extract sales and revenue for {product_name}")
])

chain_4 = prompt_4 | model | json_parser_4

result_4 = chain_4.invoke({"product_name": "Samsung S25"})
print(f"Raw JSON Result: {result_4}")
print(f"Type: {type(result_4)}")
