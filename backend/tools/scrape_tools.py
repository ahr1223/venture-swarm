"""
Scrape Tools: Live Web Scraper for VentureSwarm
Extracts actual pricing tables, headline copy, feature bullet points, and value propositions
from live competitor websites using httpx and BeautifulSoup4.
"""

import re
import logging
from typing import Dict, Any, Optional, List
import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger("ventureswarm.tools.scraper")

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

def scrape_competitor_website(url: str, timeout: float = 8.0) -> Dict[str, Any]:
    """
    Fetches and parses a competitor's website or pricing page.
    Extracts:
    - Title & Meta Description
    - H1, H2 tags (value props)
    - Pricing keywords & detected dollar amounts
    - Feature bullet points
    - Raw cleaned text summary
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    result = {
        "url": url,
        "success": False,
        "title": "",
        "meta_description": "",
        "headlines": [],
        "pricing_signals": [],
        "feature_bullets": [],
        "cleaned_snippet": "",
        "error": None
    }

    try:
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        with httpx.Client(follow_redirects=True, timeout=timeout, headers=headers) as client:
            resp = client.get(url)
            if resp.status_code >= 400:
                result["error"] = f"HTTP {resp.status_code}"
                return result

            soup = BeautifulSoup(resp.text, "html.parser")

            # Remove scripts, styles, navbars, footers to isolate core content
            for tag in soup(["script", "style", "noscript", "svg", "header", "footer"]):
                tag.extract()

            # Title
            if soup.title and soup.title.string:
                result["title"] = soup.title.string.strip()

            # Meta description
            meta_desc = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
            if meta_desc and meta_desc.get("content"):
                result["meta_description"] = meta_desc["content"].strip()

            # Headlines (H1, H2)
            headlines = []
            for h in soup.find_all(["h1", "h2"]):
                text = h.get_text(strip=True)
                if text and len(text) > 5 and len(text) < 140:
                    headlines.append(text)
            result["headlines"] = headlines[:6]

            # Pricing signals (look for $, /mo, /yr, free trial, tier names)
            text_corpus = soup.get_text(separator=" ", strip=True)
            pricing_matches = re.findall(
                r'(\$\s?\d{1,4}(?:\.\d{2})?(?:\s?/\s?(?:mo|month|yr|year|user|seat))?|free\s+trial|enterprise|contact\s+sales)',
                text_corpus,
                flags=re.IGNORECASE
            )
            # Deduplicate preserving order
            seen_pricing = set()
            clean_pricing = []
            for p in pricing_matches:
                p_clean = p.strip()
                if p_clean.lower() not in seen_pricing:
                    seen_pricing.add(p_clean.lower())
                    clean_pricing.append(p_clean)
            result["pricing_signals"] = clean_pricing[:8]

            # Feature bullets (li items with reasonable length)
            bullets = []
            for li in soup.find_all("li"):
                li_text = li.get_text(strip=True)
                if 15 < len(li_text) < 120 and not any(skip in li_text.lower() for skip in ["cookie", "terms", "privacy", "login"]):
                    bullets.append(li_text)
            result["feature_bullets"] = bullets[:10]

            # Cleaned snippet
            lines = [l.strip() for l in text_corpus.splitlines() if l.strip()]
            condensed = " ".join(lines[:30])
            result["cleaned_snippet"] = condensed[:800]
            result["success"] = True

    except Exception as e:
        logger.warning(f"Failed to scrape {url}: {e}")
        result["error"] = str(e)

    return result
