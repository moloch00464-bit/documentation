#!/usr/bin/env python3
"""
M.O.L.O.C.H. 3.0 - Web Tool
============================
Web search & fetch
"""

import requests
from typing import Optional, List, Dict
from urllib.parse import quote_plus


class WebTool:
    """
    Web Operations Tool

    Features:
    - Web search (DuckDuckGo)
    - URL fetch
    - Basic HTML parsing
    """

    def __init__(self):
        """Initialize Web Tool"""
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "M.O.L.O.C.H. 3.0 Bot"
        })

    # ═══════════════════════════════════════════════════════════════════════════
    # WEB SEARCH
    # ═══════════════════════════════════════════════════════════════════════════

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Search the web (DuckDuckGo)

        Args:
            query: Search query
            max_results: Max number of results

        Returns:
            List of results: [{"title": "...", "url": "...", "snippet": "..."}]
        """
        # Try API first (fast but sometimes empty)
        results = self._search_api(query, max_results)

        # Fallback to HTML scraping if API gave no results
        if not results:
            results = self._search_html(query, max_results)

        return results

    def _search_api(self, query: str, max_results: int) -> List[Dict[str, str]]:
        """
        DuckDuckGo Instant Answer API (fast but sometimes empty)
        """
        try:
            url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json"

            response = self.session.get(url, timeout=10)
            # Accept both 200 (OK) and 202 (Accepted) - DDG sometimes returns 202
            if response.status_code not in [200, 202]:
                return []

            data = response.json()
            results = []

            # Get instant answer
            if data.get("AbstractText"):
                results.append({
                    "title": data.get("Heading", query),
                    "url": data.get("AbstractURL", ""),
                    "snippet": data.get("AbstractText", "")[:200]
                })

            # Get related topics
            for topic in data.get("RelatedTopics", [])[:max_results]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append({
                        "title": topic.get("Text", "")[:100],
                        "url": topic.get("FirstURL", ""),
                        "snippet": topic.get("Text", "")[:200]
                    })

            return results[:max_results]

        except:
            return []

    def _search_html(self, query: str, max_results: int) -> List[Dict[str, str]]:
        """
        DuckDuckGo HTML scraping (robust fallback)
        """
        try:
            # Use DuckDuckGo HTML search
            url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"

            # DEBUG
            print(f"🔍 DEBUG: Fetching {url}")

            response = self.session.get(url, timeout=10)

            # DEBUG
            print(f"🔍 DEBUG: Status code: {response.status_code}")
            print(f"🔍 DEBUG: Response length: {len(response.text)} chars")

            if response.status_code != 200:
                return []

            html = response.text
            results = []

            # Simple regex-based extraction (no BeautifulSoup dependency)
            import re

            # Find result blocks
            # Pattern: <a class="result__a" href="URL">TITLE</a>
            # Then later: <a class="result__snippet">SNIPPET</a>

            pattern = r'class="result__a"[^>]+href="([^"]+)"[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, html)

            # DEBUG
            print(f"🔍 DEBUG: Found {len(matches)} title matches")

            snippet_pattern = r'class="result__snippet">([^<]+)</a>'
            snippets = re.findall(snippet_pattern, html)

            # DEBUG
            print(f"🔍 DEBUG: Found {len(snippets)} snippet matches")

            for i, (url, title) in enumerate(matches[:max_results]):
                snippet = snippets[i] if i < len(snippets) else ""

                results.append({
                    "title": title.strip(),
                    "url": url.strip(),
                    "snippet": snippet.strip()[:200]
                })

                # DEBUG
                if i == 0:
                    print(f"🔍 DEBUG: First result: {title[:50]}...")

            return results

        except requests.exceptions.Timeout:
            print("⚠️ Search timeout")
            return []
        except Exception as e:
            print(f"⚠️ HTML search fallback failed: {e}")
            import traceback
            traceback.print_exc()
            return []

    # ═══════════════════════════════════════════════════════════════════════════
    # URL FETCH
    # ═══════════════════════════════════════════════════════════════════════════

    def fetch(self, url: str, timeout: int = 15) -> Optional[str]:
        """
        Fetch URL content

        Args:
            url: URL to fetch
            timeout: Request timeout

        Returns:
            Page content or None
        """
        try:
            response = self.session.get(url, timeout=timeout)

            if response.status_code != 200:
                print(f"⚠️ HTTP {response.status_code}: {url}")
                return None

            # Get content
            content = response.text

            # Basic cleaning (remove excessive whitespace)
            import re
            content = re.sub(r'\s+', ' ', content)

            return content

        except requests.exceptions.Timeout:
            print(f"⚠️ Fetch timeout: {url}")
            return None
        except Exception as e:
            print(f"❌ Fetch error: {e}")
            return None

    def fetch_text_only(self, url: str) -> Optional[str]:
        """
        Fetch URL and extract text only (no HTML tags)

        Args:
            url: URL to fetch

        Returns:
            Plain text content or None
        """
        content = self.fetch(url)
        if not content:
            return None

        # Remove HTML tags (simple approach)
        import re
        text = re.sub(r'<[^>]+>', '', content)

        # Clean whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        return text

    # ═══════════════════════════════════════════════════════════════════════════
    # HELPERS
    # ═══════════════════════════════════════════════════════════════════════════

    def is_url_alive(self, url: str) -> bool:
        """
        Check if URL is accessible

        Args:
            url: URL to check

        Returns:
            True if accessible, False otherwise
        """
        try:
            response = self.session.head(url, timeout=5)
            return response.status_code < 400
        except:
            return False


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🌐 M.O.L.O.C.H. 3.0 Web Tool Test\n")

    web = WebTool()

    # Test search
    print("🔍 Testing web search...")
    results = web.search("Python programming", max_results=3)
    print(f"   ✅ Found {len(results)} results")
    if results:
        print(f"   First: {results[0].get('title', 'N/A')[:50]}...")

    # Test URL check
    print("\n🌐 Testing URL check...")
    is_alive = web.is_url_alive("https://www.google.com")
    print(f"   {'✅' if is_alive else '❌'} google.com: {is_alive}")

    # Note: Fetch test skipped to avoid unnecessary requests
    print("\n💡 Fetch test skipped (use manually to avoid unnecessary requests)")

    print()
