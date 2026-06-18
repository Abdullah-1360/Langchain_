"""LangGraph workflow for the research assistant"""
from typing import Any, Dict
from langgraph.graph import StateGraph, START, END
from langgraph.types import StateSnapshot
from pydantic import BaseModel, Field
from agents.researcher import ResearcherAgent
from agents.analyst import AnalystAgent
from config.settings import MAX_ITERATIONS


class ResearchState(BaseModel):
    """State for the research workflow"""
    query: str
    research_data: Dict[str, Any] = Field(default_factory=dict)
    analysis_data: Dict[str, Any] = Field(default_factory=dict)
    iterations: int = 0
    status: str = "initialized"
    errors: list = Field(default_factory=list)


class ResearchGraph:
    """LangGraph workflow for multi-agent research"""
    
    def __init__(self):
        """Initialize the research graph"""
        self.researcher = ResearcherAgent()
        self.analyst = AnalystAgent()
        self.graph = self._build_graph()
        self.compiled_graph = self.graph.compile()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        graph = StateGraph(ResearchState)
        
        # Add nodes
        graph.add_node("research", self._research_node)
        graph.add_node("analyze", self._analyze_node)
        graph.add_node("review", self._review_node)
        
        # Add edges
        graph.add_edge(START, "research")
        graph.add_conditional_edges(
            "research",
            self._should_analyze,
            {
                "analyze": "analyze",
                "end": END
            }
        )
        graph.add_conditional_edges(
            "analyze",
            self._should_review,
            {
                "review": "review",
                "end": END
            }
        )
        graph.add_edge("review", END)
        
        return graph
    
    def _research_node(self, state: ResearchState) -> Dict[str, Any]:
        """Research node - gathers information"""
        print(f"\n🔍 [Research Phase] Researching: {state.query}")
        
        research_result = self.researcher.execute({"query": state.query})
        
        return {
            "research_data": research_result,
            "status": "research_completed",
            "iterations": state.iterations + 1
        }
    
    def _analyze_node(self, state: ResearchState) -> Dict[str, Any]:
        """Analyze node - analyzes research data"""
        print("\n📊 [Analysis Phase] Analyzing research data...")
        
        synthesis = state.research_data.get("synthesized_info", "")
        analysis_result = self.analyst.execute({"research_data": synthesis})
        
        return {
            "analysis_data": analysis_result,
            "status": "analysis_completed",
            "iterations": state.iterations + 1
        }
    
    def _review_node(self, state: ResearchState) -> Dict[str, Any]:
        """Review node - generates final report"""
        print("\n✅ [Review Phase] Finalizing report...")
        
        return {
            "status": "completed",
            "iterations": state.iterations + 1
        }
    
    def _should_analyze(self, state: ResearchState) -> str:
        """Determine if we should move to analysis phase"""
        if state.status == "research_completed" and state.research_data:
            return "analyze"
        return "end"
    
    def _should_review(self, state: ResearchState) -> str:
        """Determine if we should move to review phase"""
        if state.status == "analysis_completed" and state.analysis_data:
            return "review"
        return "end"
    
    def run(self, query: str) -> Dict[str, Any]:
        """Run the research workflow"""
        print("\n" + "="*80)
        print("🚀 Starting Multi-Agent Research Assistant")
        print("="*80)
        
        initial_state = ResearchState(query=query)
        
        try:
            final_state = self.compiled_graph.invoke(initial_state)

            if isinstance(final_state, dict):
                research_data = final_state.get("research_data", {})
                analysis_data = final_state.get("analysis_data", {})
                iterations = final_state.get("iterations", 0)
            else:
                research_data = getattr(final_state, "research_data", {})
                analysis_data = getattr(final_state, "analysis_data", {})
                iterations = getattr(final_state, "iterations", 0)

            return {
                "success": True,
                "query": query,
                "research": research_data,
                "analysis": analysis_data,
                "iterations": iterations
            }
        except Exception as e:
            print(f"❌ Error during workflow: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }
