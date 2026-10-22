"""
Market Researcher Agent (Codename: Scout)
Analyzes the raw business idea, synthesizes market keywords, and runs live web search queries.
"""

import json
import logging
from typing import Dict, Any, List
from backend.tools.search_tools import search_market_and_competitors
from backend.llm.client import LLMClient

logger = logging.getLogger("ventureswarm.agents.researcher")

class MarketResearcherAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def run(self, raw_idea: str, emit_thought) -> Dict[str, Any]:
        """
        Executes market discovery:
        1. Formulates search queries
        2. Dispatches live DuckDuckGo searches
        3. Identifies competitor candidates and industry landscape
        """
        emit_thought("Scout", "Deconstructing raw business concept into core market mechanics...", "active")

        system_prompt = (
            "You are Scout, an elite Venture Capital Market Intelligence AI. "
            "Your job is to deconstruct a raw startup idea, identify the exact target industry, "
            "value proposition, and craft 3 precise search queries to locate direct competitors."
        )

        user_prompt = f"""
Raw Business Idea:
\"\"\"{raw_idea}\"\"\"

Provide a JSON object with:
{{
  "sector": "e.g. B2B SaaS, DevTools, E-commerce, FinTech",
  "core_value_prop": "Concise 1-sentence value proposition",
  "category_keywords": ["keyword1", "keyword2", "keyword3"],
  "search_queries": [
    "query to find top competitors",
    "query to find competitor pricing and alternatives",
    "query to find user pain points / forum discussions"
  ]
}}
"""
        response_text = self.llm.generate(system_prompt, user_prompt, response_format="json")

        parsed = {}
        try:
            # Clean markdown codeblocks if present
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            parsed = json.loads(cleaned)
        except Exception:
            # Fallback domain-grounded synthesis
            from backend.agents.domain_extractor import analyze_idea_domain
            domain_info = analyze_idea_domain(raw_idea)
            key_kw = domain_info["sector"].split("&")[0].strip().lower()
            parsed = {
                "sector": domain_info["sector"],
                "core_value_prop": f"Autonomous platform that {domain_info['solution']}",
                "category_keywords": [key_kw, "automation", "advisory"],
                "search_queries": [
                    f"{key_kw} competitors alternatives",
                    f"{key_kw} pricing plans",
                    f"best {key_kw} software for business"
                ]
            }

        queries = parsed.get("search_queries", [f"{raw_idea[:30]} competitors"])
        emit_thought("Scout", f"Generated {len(queries)} market radar search vectors. Querying live web index...", "active")

        # Execute Live DuckDuckGo Searches
        search_hits: List[Dict[str, str]] = []
        for q in queries[:2]:
            emit_thought("Scout", f"Searching web: '{q}'", "tool")
            hits = search_market_and_competitors(q, max_results=4)
            for h in hits:
                if not any(existing["href"] == h["href"] for existing in search_hits):
                    search_hits.append(h)

        emit_thought("Scout", f"Discovered {len(search_hits)} live market signals and competitor domains.", "completed")

        return {
            "sector": parsed.get("sector", "Technology / SaaS"),
            "core_value_prop": parsed.get("core_value_prop", raw_idea),
            "category_keywords": parsed.get("category_keywords", []),
            "search_queries": queries,
            "search_hits": search_hits
        }
