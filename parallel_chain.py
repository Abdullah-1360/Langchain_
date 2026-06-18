
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser,StrOutputParser
from langchain_core.runnables import RunnableParallel
load_dotenv()

# Same model setup as output_parsing.py
API_URL = "http://127.0.0.1:8080/v1"

model_1 = ChatOpenAI(
    base_url=API_URL,
    api_key="not-needed",
    model="Qwen3-4B-Q4_K_M",
    max_tokens=2048,
    temperature=0,
)
model_2 = ChatOpenAI(
    base_url=API_URL,
    api_key="not-needed",
    model="Qwen3-4B-Q4_K_M",
    max_tokens=2048,
    temperature=0,
)


prompt1 = PromptTemplate(
    input_variables=["input"],
    template="generate a short story on the topic {input}"
)
prompt2 = PromptTemplate(
    input_variables=["input"],
    template="generate 5 questions quiz with answers from following text:\n {input}"
)


final_prompt = PromptTemplate(
    input_variables=["quiz","notes"],
    template="Merge the following two outputs ->\n {quiz}\n{notes} \n into a single quiz with notes output"
)


parser = StrOutputParser()

parallel_chain = RunnableParallel({
    "quiz": prompt1 | model_1 | parser,
    "notes": prompt2 | model_2 | parser
})

chain = parallel_chain | final_prompt | model_1 | parser
text = """"Global warming is one of the most significant environmental challenges facing the world today.
It refers to the gradual increase in Earth's average temperature due to the buildup of greenhouse gases,
such as carbon dioxide, methane, and nitrous oxide, in the atmosphere. These gases trap heat from the sun,
creating a greenhouse effect that warms the planet. Human activities, particularly the burning of fossil
fuels for energy, transportation, and industrial production, are the primary contributors to this phenomenon.
Deforestation also plays a major role, as trees absorb carbon dioxide and help regulate the climate. 
As global temperatures continue to rise, the effects of global warming are becoming increasingly visible.
Glaciers and polar ice caps are melting at an alarming rate, leading to rising sea levels that threaten 
coastal communities and ecosystems. Extreme weather events, including heatwaves, droughts, floods, and
powerful storms, are occurring more frequently and with greater intensity. These changes have serious
consequences for agriculture, water resources, biodiversity, and human health. Many plant and animal 
species struggle to adapt to rapidly changing conditions, increasing the risk of extinction and 
disrupting natural ecosystems. Furthermore, global warming can contribute to food insecurity by 
reducing crop yields and affecting livestock production in vulnerable regions. The economic costs 
associated with climate-related disasters are also growing, placing significant pressure on
governments and communities worldwide. Addressing global warming requires collective action 
at local, national, and international levels. Governments can implement policies that promote 
renewable energy sources such as solar, wind, and hydroelectric power while reducing dependence
on fossil fuels. Individuals can also contribute by conserving energy, using public 
transportation, reducing waste, and supporting environmentally sustainable practices.
International cooperation is essential because climate change affects all countries 
regardless of their level of development. Agreements and partnerships can help nations
work together to reduce greenhouse gas emissions and develop innovative solutions for
a more sustainable future. Although global warming presents a complex and urgent challenge, 
scientific advancements, public awareness, and coordinated efforts offer hope for mitigating its impacts.
 By taking responsible action today, humanity can help protect the environment, preserve natural resources, 
 and ensure a healthier and more stable planet for future generations.
"""
print(chain.invoke({"input": text}))
chain.get_graph().render("parallel_chain_graph", format="png", view=True)