"""
Search Tools: Live Web Discovery for VentureSwarm
Uses DuckDuckGo Search (ddgs) to find live competitors, pricing pages, and market discussions.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger("ventureswarm.tools.search")

def search_market_and_competitors(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Executes live web search using ddgs with intelligent fallback keywords.
    Returns list of dicts with title, href, and snippet.
    """
    results = []
    
    # Try ddgs first
    try:
        from ddgs import DDGS
        ddgs = DDGS()
        raw = list(ddgs.text(query, max_results=max_results))
        for item in raw:
            results.append({
                "title": item.get("title", ""),
                "href": item.get("href", ""),
                "snippet": item.get("body", item.get("snippet", ""))
            })
        if results:
            return results
    except Exception as e:
        logger.warning(f"ddgs search failed for query '{query}': {e}")
    
    # Try duckduckgo_search fallback
    try:
        from duckduckgo_search import DDGS as LegacyDDGS
        raw = list(LegacyDDGS().text(query, max_results=max_results))
        for item in raw:
            results.append({
                "title": item.get("title", ""),
                "href": item.get("href", ""),
                "snippet": item.get("body", item.get("snippet", ""))
            })
        if results:
            return results
    except Exception as e:
        logger.warning(f"Legacy duckduckgo_search failed for query '{query}': {e}")
        
    return results

def find_competitor_pricing_pages(competitor_domain_or_name: str) -> List[Dict[str, str]]:
    """
    Discovers specific pricing, feature, or review pages for a competitor.
    """
    query = f"{competitor_domain_or_name} pricing plans features"
    return search_market_and_competitors(query, max_results=3)
