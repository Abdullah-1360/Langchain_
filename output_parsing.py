import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
from typing import TypedDict,Annotated,Optional,Literal

load_dotenv()

# Define the TypedDict template
class Review(TypedDict):
    key_themes:Annotated[list[str],"write down all the key themes mentioned in review into a list"]
    summary: Annotated[str,"A brief summary of review"]
    sentiment: Annotated[Literal["pos","neg","neut"],"Sentiment must be negative,positive or neutral"]
    pros:Annotated[Optional[list[str]],"write down all the pros inside a list"]
    cons:Annotated[Optional[list[str]],"write down all the cons inside a list"]

# Pointing to your background llama-server loop on port 8080
API_URL = "http://127.0.0.1:8080/v1"

model = ChatOpenAI(
    base_url=API_URL,
    api_key="not-needed",
    model="Qwen3-8B-Q6_K", # Updated matching your currently active background model
    max_tokens=2048,
    temperature=0.1,  # Low temperature guarantees strict adherence to schema keys
)

# Crucial Fix: Forcing function_calling ensures local llama-server handles it seamlessly
structure_model = model.with_structured_output(Review, method="json_schema")

review_text = """The Samsung Galaxy S25 Ultra is the latest flagship smartphone from Samsung, continuing the legacy of the S24 Ultra
 with incremental improvements and new features. 
While it offers a compelling mix of performance, display quality, and camera capabilities, 
it also comes with some drawbacks that potential buyers should consider.
The Samsung Galaxy S25 Ultra is a strong contender in the flagship smartphone market, offering top-tier hardware 
and a premium experience. However, its high cost and lack of major design changes may make it less appealing to some users. 
Its best suited for those who prioritize performance, display quality, and camera capabilities.

Pros
Powerful Performance: Equipped with the latest Snapdragon 8 Gen 3 or Exynos 2400 chipset, the S25 Ultra delivers top-tier performance for demanding tasks, gaming, and multitasking.
Exceptional Display: The 6.8-inch Dynamic AMOLED 2X display offers vibrant colors, high brightness, and a 120Hz refresh rate, making it ideal for media consumption and gaming.
Advanced Camera System: The S25 Ultra features a 200MP main camera, a 50MP ultra-wide lens, and a 10MP periscope telephoto lens, offering excellent zoom capabilities and image quality in various lighting conditions.
Long-Lasting Battery: The large battery capacity and optimized power management ensure all-day usage without frequent charging.
Premium Build Quality: The device features a sleek, durable design with Gorilla Glass Victus 3 and a metal frame, giving it a premium feel.
Software Features: One UI 6.1 brings improved customization, enhanced multitasking, and better integration with Samsung’s ecosystem.
Cons
High Price Point: The S25 Ultra is one of the most expensive flagship phones on the market, which may not be justified for users who don’t need the latest features.
Limited Storage Options: The base model comes with 256GB of storage, and higher capacities are not available, which may be a drawback for heavy users.
Battery Life Not as Long as Expected: Despite the large battery, some users report that the battery life is not as long as previous models, especially with heavy usage.
Camera Software Can Be Overly Complex: The camera app offers a lot of features, but some users find it overwhelming and may prefer simpler interfaces.
No Major Design Changes: Compared to the S24 Ultra, the S25 Ultra has a similar design, which may feel repetitive to some users.
Software Bloat: One UI includes many features, some of which may be unnecessary for casual users, leading to a cluttered experience.
"""
messages = [
    SystemMessage(content=(
        "You are a precise data extraction assistant. Analyze the user's review "
        "and extract the key themes, summary, sentiment, pros, and cons strictly "
        "matching the requested schema format."
    )),
    HumanMessage(content=review_text)
]
print("Processing review output format natively...")
result = structure_model.invoke(messages)

print("\n--- Final Structured Result ---")
print(result)
print(f"Type of output: {type(result)}")