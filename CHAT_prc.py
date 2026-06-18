from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
model= ChatOpenAI(model= 'gpt-4o-mini')
print(model.invoke("capital of Pakistan").content)
