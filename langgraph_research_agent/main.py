"""Main entry point for the LangGraph Research Assistant"""
import sys
from graph.research_graph import ResearchGraph
from utils.output_formatting import format_research_output, format_analysis_output


def main():
    """Main function to run the research assistant"""
    
    # Example queries to demonstrate the system
    queries = [
        "What are the latest developments in artificial intelligence in 2024?",
        "How is climate change affecting global agriculture?",
    ]
    
    # Initialize the research graph
    research_graph = ResearchGraph()
    
    # Run for the first query as an example
    query = queries[0]
    
    print("\n" + "="*80)
    print("📝 QUERY: " + query)
    print("="*80)
    
    # Execute the workflow
    result = research_graph.run(query)
    
    if result["success"]:
        # Display research results
        research_output = format_research_output(result["research"])
        print(research_output)
        
        # Display analysis results
        if result["analysis"]:
            analysis_output = format_analysis_output(result["analysis"])
            print(analysis_output)
        
        print(f"\n✅ Workflow completed in {result['iterations']} iterations")
    else:
        print(f"\n❌ Error: {result['error']}")


def interactive_mode():
    """Run in interactive mode - accept user queries"""
    research_graph = ResearchGraph()
    
    print("\n" + "="*80)
    print("🤖 Multi-Agent Research Assistant")
    print("="*80)
    print("Enter your research query (or 'exit' to quit):\n")
    
    while True:
        query = input("\n📝 Query: ").strip()
        
        if query.lower() == 'exit':
            print("\nGoodbye! 👋")
            break
        
        if not query:
            print("Please enter a valid query.")
            continue
        
        result = research_graph.run(query)
        
        if result["success"]:
            research_output = format_research_output(result["research"])
            print(research_output)
            
            if result["analysis"]:
                analysis_output = format_analysis_output(result["analysis"])
                print(analysis_output)
            
            print(f"\n✅ Completed in {result['iterations']} iterations")
        else:
            print(f"\n❌ Error: {result['error']}")


if __name__ == "__main__":
    # Check if running in interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        # Run with example queries
        main()
