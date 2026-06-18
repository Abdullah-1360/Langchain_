"""Search tools for gathering information"""
from typing import List
from config.settings import MAX_SEARCH_RESULTS

try:
    from duckduckgo_search import DDGS
    SEARCH_AVAILABLE = True
except ImportError:
    SEARCH_AVAILABLE = False


def search_information(query: str) -> List[str]:
    """
    Search for information about a query using DuckDuckGo
    
    Args:
        query: Search query string
    
    Returns:
        List of search results
    """
    if not SEARCH_AVAILABLE:
        # Fallback mock results if duckduckgo_search not available
        return get_mock_results(query)
    
    try:
        results = []
        ddgs = DDGS()
        search_results = ddgs.text(query, max_results=MAX_SEARCH_RESULTS)
        
        for result in search_results:
            formatted_result = f"Title: {result.get('title', 'N/A')}\n"
            formatted_result += f"Body: {result.get('body', 'N/A')}\n"
            formatted_result += f"Link: {result.get('href', 'N/A')}"
            results.append(formatted_result)
        
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return get_mock_results(query)


def get_mock_results(query: str) -> List[str]:
    """Get mock search results for demonstration"""
    mock_results = [
        f"Information about '{query}' - Result 1: Key findings and data related to your search.",
        f"Information about '{query}' - Result 2: Additional insights and context.",
        f"Information about '{query}' - Result 3: Related information and references.",
    ]
    return mock_results
