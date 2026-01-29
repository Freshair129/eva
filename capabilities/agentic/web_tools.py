"""
Web Tools - Internet access for EVA.
Security Level: L3 (Remote - Requires Confirmation + Sandbox)

Supported Search Providers:
1. DuckDuckGo (free, no API key required) - DEFAULT
2. Serper.dev (paid, fast Google results) - Set SERPER_API_KEY env var
3. SerpAPI (paid, comprehensive) - Set SERPAPI_KEY env var
"""

import logging
import os
import json
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus, urlencode
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)

# Default timeout for web requests
DEFAULT_TIMEOUT = 10


def _search_duckduckgo(query: str, limit: int = 5) -> Dict[str, Any]:
    """
    Search using DuckDuckGo Instant Answer API (free, no key required).
    Note: This API returns instant answers, not full web search results.
    """
    try:
        url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1"
        
        req = urllib.request.Request(url, headers={"User-Agent": "EVA-Agent/0.1"})
        
        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as response:
            data = json.loads(response.read().decode("utf-8"))
        
        results = []
        
        # Abstract (main answer)
        if data.get("Abstract"):
            results.append({
                "title": data.get("Heading", "DuckDuckGo Answer"),
                "url": data.get("AbstractURL", ""),
                "snippet": data.get("Abstract", "")
            })
        
        # Related Topics
        for topic in data.get("RelatedTopics", [])[:limit-1]:
            if isinstance(topic, dict) and "Text" in topic:
                results.append({
                    "title": topic.get("Text", "")[:80],
                    "url": topic.get("FirstURL", ""),
                    "snippet": topic.get("Text", "")
                })
        
        return {
            "status": "success",
            "provider": "duckduckgo",
            "query": query,
            "results": results[:limit],
            "total": len(results)
        }
        
    except Exception as e:
        logger.error(f"DuckDuckGo search error: {e}")
        return {"status": "error", "provider": "duckduckgo", "message": str(e)}


def _search_serper(query: str, limit: int = 5, api_key: str = None) -> Dict[str, Any]:
    """
    Search using Serper.dev API (Google results, requires API key).
    Get free API key at: https://serper.dev
    """
    try:
        api_key = api_key or os.environ.get("SERPER_API_KEY")
        
        if not api_key:
            return {
                "status": "error",
                "provider": "serper",
                "message": "SERPER_API_KEY not set. Get free key at https://serper.dev"
            }
        
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        payload = json.dumps({"q": query, "num": limit}).encode("utf-8")
        
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        
        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as response:
            data = json.loads(response.read().decode("utf-8"))
        
        results = []
        
        # Organic results
        for item in data.get("organic", [])[:limit]:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", "")
            })
        
        return {
            "status": "success",
            "provider": "serper",
            "query": query,
            "results": results,
            "total": len(results)
        }
        
    except Exception as e:
        logger.error(f"Serper search error: {e}")
        return {"status": "error", "provider": "serper", "message": str(e)}


def _search_serpapi(query: str, limit: int = 5, api_key: str = None) -> Dict[str, Any]:
    """
    Search using SerpAPI (comprehensive, requires API key).
    Get API key at: https://serpapi.com
    """
    try:
        api_key = api_key or os.environ.get("SERPAPI_KEY")
        
        if not api_key:
            return {
                "status": "error", 
                "provider": "serpapi",
                "message": "SERPAPI_KEY not set. Get key at https://serpapi.com"
            }
        
        params = urlencode({
            "q": query,
            "api_key": api_key,
            "engine": "google",
            "num": limit
        })
        url = f"https://serpapi.com/search?{params}"
        
        req = urllib.request.Request(url, headers={"User-Agent": "EVA-Agent/0.1"})
        
        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as response:
            data = json.loads(response.read().decode("utf-8"))
        
        results = []
        
        for item in data.get("organic_results", [])[:limit]:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", "")
            })
        
        return {
            "status": "success",
            "provider": "serpapi",
            "query": query,
            "results": results,
            "total": len(results)
        }
        
    except Exception as e:
        logger.error(f"SerpAPI search error: {e}")
        return {"status": "error", "provider": "serpapi", "message": str(e)}


def web_search(
    query: str,
    limit: int = 5,
    provider: str = "auto",
    _confirmed: bool = False,
    _api_key: str = None
) -> Dict[str, Any]:
    """
    Searches the internet using available search APIs.
    Security Level: L3 (Remote - Requires Confirmation)
    
    Args:
        query: Search query string
        limit: Maximum number of results (default: 5)
        provider: Search provider ("auto", "duckduckgo", "serper", "serpapi")
        _confirmed: Internal flag for confirmation bypass
        _api_key: Optional API key override
        
    Returns:
        Dictionary with search results or confirmation request
        
    Providers:
        - duckduckgo: Free, no API key (instant answers only)
        - serper: Fast Google results, requires SERPER_API_KEY
        - serpapi: Comprehensive, requires SERPAPI_KEY
        - auto: Try serper -> serpapi -> duckduckgo
    """
    # Check confirmation
    if not _confirmed:
        return {
            "status": "pending_confirmation",
            "action": "web_search",
            "query": query,
            "provider": provider,
            "message": f"Request to search the web for: '{query}'. This will make an external API call. Confirm?"
        }
    
    try:
        # Provider selection
        if provider == "duckduckgo":
            return _search_duckduckgo(query, limit)
        elif provider == "serper":
            return _search_serper(query, limit, _api_key)
        elif provider == "serpapi":
            return _search_serpapi(query, limit, _api_key)
        elif provider == "auto":
            # Try providers in order of quality
            
            # 1. Try Serper if key available
            if os.environ.get("SERPER_API_KEY") or _api_key:
                result = _search_serper(query, limit, _api_key)
                if result["status"] == "success":
                    return result
            
            # 2. Try SerpAPI if key available  
            if os.environ.get("SERPAPI_KEY"):
                result = _search_serpapi(query, limit)
                if result["status"] == "success":
                    return result
            
            # 3. Fallback to DuckDuckGo (free)
            return _search_duckduckgo(query, limit)
        else:
            return {"status": "error", "message": f"Unknown provider: {provider}"}
        
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
