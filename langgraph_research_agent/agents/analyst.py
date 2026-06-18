"""Analyst agent for analyzing and generating insights"""
from typing import Any, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .base_agent import BaseAgent


class AnalystAgent(BaseAgent):
    """Agent responsible for analyzing information and generating insights"""
    
    def __init__(self):
        super().__init__("Analyst")
        self.analysis_prompt = ChatPromptTemplate.from_template(
            """You are a senior analyst. Analyze the following research data and provide:

1. Key Insights: Most important findings
2. Patterns: Recurring themes or patterns
3. Gaps: Missing information or areas for further research
4. Recommendations: Actionable recommendations based on findings
5. Confidence Level: How confident are you in these conclusions (0-100%)

Research Data:
{research_data}

Provide a detailed analysis with clear structure."""
        )
        
        self.summary_prompt = ChatPromptTemplate.from_template(
            """Create an executive summary of the following analysis:

Analysis:
{analysis}

The summary should be concise (2-3 paragraphs) and highlight the most important points."""
        )
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the analysis process"""
        research_data = input_data.get("research_data", "")
        
        if not research_data:
            return {"error": "No research data provided", "analysis": None}
        
        # Step 1: Perform analysis
        analysis_chain = self.analysis_prompt | self.llm | StrOutputParser()
        analysis = analysis_chain.invoke({"research_data": research_data})
        
        # Step 2: Create summary
        summary_chain = self.summary_prompt | self.llm | StrOutputParser()
        summary = summary_chain.invoke({"analysis": analysis})
        
        return {
            "detailed_analysis": analysis,
            "summary": summary,
            "status": "completed"
        }
