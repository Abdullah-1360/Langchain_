"""Output formatting utilities"""
from typing import Dict, Any
import json


def format_research_output(result: Dict[str, Any]) -> str:
    """Format research output for display"""
    output = "\n" + "="*80 + "\n"
    output += "RESEARCH RESULTS\n"
    output += "="*80 + "\n\n"
    
    if "error" in result:
        output += f"Error: {result['error']}\n"
    else:
        output += f"Query: {result.get('query', 'N/A')}\n\n"
        output += "Research Plan:\n"
        output += "-" * 40 + "\n"
        output += result.get('research_plan', 'N/A') + "\n\n"
        
        output += "Synthesized Information:\n"
        output += "-" * 40 + "\n"
        output += result.get('synthesized_info', 'N/A') + "\n"
    
    output += "\n" + "="*80 + "\n"
    return output


def format_analysis_output(result: Dict[str, Any]) -> str:
    """Format analysis output for display"""
    output = "\n" + "="*80 + "\n"
    output += "ANALYSIS RESULTS\n"
    output += "="*80 + "\n\n"
    
    if "error" in result:
        output += f"Error: {result['error']}\n"
    else:
        output += "Executive Summary:\n"
        output += "-" * 40 + "\n"
        output += result.get('summary', 'N/A') + "\n\n"
        
        output += "Detailed Analysis:\n"
        output += "-" * 40 + "\n"
        output += result.get('detailed_analysis', 'N/A') + "\n"
    
    output += "\n" + "="*80 + "\n"
    return output


def save_results(results: Dict[str, Any], filename: str = "results.json"):
    """Save results to a JSON file"""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {filename}")
