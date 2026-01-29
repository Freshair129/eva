"""
Web Tools - Internet access for EVA.
Security Level: L3 (Remote - Requires Confirmation + Sandbox)
"""

import logging
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)


def web_search(
    query: str,
    limit: int = 5,
    _confirmed: bool = False,
    _api_key: str = None
) -> Dict[str, Any]:
    """
    Searches the internet using a search API.
    Security Level: L3 (Remote - Requires Confirmation)
    
    Args:
        query: Search query string
        limit: Maximum number of results (default: 5)
        _confirmed: Internal flag for confirmation bypass
        _api_key: API key for search service (injected at runtime)
        
    Returns:
        Dictionary with search results or confirmation request
    """
    # Check confirmation
    if not _confirmed:
        return {
            "status": "pending_confirmation",
            "action": "web_search",
            "query": query,
            "message": f"Request to search the web for: '{query}'. This will make an external API call. Confirm?"
        }
    
    try:
        # Mock implementation for Phase 3
        # In production, this would call Serper, Google, or DuckDuckGo API
        
        logger.info(f"Web search (mock): {query}")
        
        # Return mock results structure
        return {
            "status": "success",
            "query": query,
            "results": [
                {
                    "title": f"[Mock Result 1 for '{query}']",
                    "url": f"https://example.com/search?q={quote_plus(query)}",
                    "snippet": "This is a mock search result. Implement actual API integration."
                }
            ],
            "total": 1,
            "note": "Mock implementation - integrate real search API for production"
        }
        
    except Exception as e:
        logger.error(f"Web search error: {e}")
        return {"status": "error", "message": str(e)}


def fetch_url(
    url: str,
    _confirmed: bool = False,
    timeout: int = 10
) -> Dict[str, Any]:
    """
    Fetches content from a URL.
    Security Level: L3 (Remote - Requires Confirmation)
    
    Args:
        url: URL to fetch
        _confirmed: Internal flag for confirmation bypass
        timeout: Request timeout in seconds
        
    Returns:
        Dictionary with fetched content or confirmation request
    """
    # Check confirmation
    if not _confirmed:
        return {
            "status": "pending_confirmation",
            "action": "fetch_url",
            "url": url,
            "message": f"Request to fetch URL: {url}. This will make an external request. Confirm?"
        }
    
    try:
        import urllib.request
        import urllib.error
        
        # Basic URL validation
        if not url.startswith(("http://", "https://")):
            return {"status": "error", "message": "URL must start with http:// or https://"}
        
        # Fetch with timeout
        req = urllib.request.Request(url, headers={"User-Agent": "EVA-Agent/0.1"})
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read().decode("utf-8", errors="replace")
            
            return {
                "status": "success",
                "url": url,
                "content_type": response.headers.get("Content-Type", "unknown"),
                "content_length": len(content),
                "content": content[:10000]  # Limit content size
            }
            
    except urllib.error.URLError as e:
        return {"status": "error", "message": f"URL Error: {str(e)}"}
    except Exception as e:
        logger.error(f"Fetch URL error: {e}")
        return {"status": "error", "message": str(e)}
