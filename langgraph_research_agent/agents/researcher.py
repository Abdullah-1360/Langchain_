"""Researcher agent for gathering information"""
from typing import Any, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .base_agent import BaseAgent
from utils.search_tools import search_information


class ResearcherAgent(BaseAgent):
    """Agent responsible for researching and gathering information"""
    
    def __init__(self):
        super().__init__("Researcher")
        self.search_prompt = ChatPromptTemplate.from_template(
            """You are a research expert. Analyze the following query and provide:
1. Key information needed
2. Search terms to use
3. Expected sources

Query: {query}

Provide a structured research plan."""
        )
        self.synthesis_prompt = ChatPromptTemplate.from_template(
            """Synthesize the following search results into a comprehensive summary:

Query: {query}

Search Results:
{search_results}

Provide a well-structured summary with key findings and sources."""
        )
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the research process"""
        query = input_data.get("query", "")
        
        if not query:
            return {"error": "No query provided", "research_data": None}
        
        # Step 1: Create research plan
        chain = self.search_prompt | self.llm | StrOutputParser()
        research_plan = chain.invoke({"query": query})
        
        # Step 2: Perform searches
        search_results = search_information(query)
        
        # Step 3: Synthesize results
        synthesis_chain = self.synthesis_prompt | self.llm | StrOutputParser()
        synthesized_info = synthesis_chain.invoke({
            "query": query,
            "search_results": "\n".join(search_results)
        })
        
        return {
            "query": query,
            "research_plan": research_plan,
            "raw_results": search_results,
            "synthesized_info": synthesized_info,
            "status": "completed"
        }
