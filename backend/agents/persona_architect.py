"""
Persona & Target Demographic Architect Agent (Codename: Demographer)
Builds deep Ideal Customer Profiles (ICP), bleeding pain points, buyer psychology,
and trigger events that drive immediate buying decisions.
"""

import json
import logging
from typing import Dict, Any
from backend.llm.client import LLMClient

logger = logging.getLogger("ventureswarm.agents.demographer")

class PersonaArchitectAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def run(self, raw_idea: str, market_data: Dict[str, Any], competitor_data: Dict[str, Any], emit_thought) -> Dict[str, Any]:
        emit_thought("Demographer", "Analyzing buyer psychology, economic incentives, and trigger events...", "active")

        system_prompt = (
            "You are Demographer, a master Go-To-Market strategist and behavioral psychologist. "
            "Synthesize an ultra-specific, high-converting B2B/B2C Ideal Customer Profile (ICP). "
            "Avoid generic buzzwords. Focus on acute bleeding pain points, purchasing authority, "
            "and emotional triggers that compel them to pull out a credit card."
        )

        user_prompt = f"""
Startup Concept:
\"\"\"{raw_idea}\"\"\"

Sector: {market_data.get('sector', 'SaaS')}
Competitor Weaknesses: {competitor_data.get('market_whitespace', 'High manual overhead')}

Generate a JSON object:
{{
  "icp_title": "Primary Decision Maker Job Title (e.g. Head of Growth, Solo Agency Founder, VP Sales)",
  "company_profile": {{
    "size": "e.g. 5-50 employees / seed-stage or solo operators",
    "annual_revenue": "e.g. $500k - $5M ARR",
    "industry": "Specific vertical"
  }},
  "acute_pain_points": [
    "Pain 1: Exact daily bottleneck costing them money or sleep",
    "Pain 2: Frustration with current competitor tools",
    "Pain 3: Risk of falling behind or losing deals"
  ],
  "purchasing_triggers": [
    "Trigger 1: Specific event that forces them to search for a solution right now",
    "Trigger 2: Budget reallocation or headcount constraint"
  ],
  "key_objections": [
    {{"objection": "What they will say to resist buying", "counter_proof": "How we instantly dismantle this doubt"}},
    {{"objection": "Second common objection", "counter_proof": "Proof point or zero-risk offer"}}
  ],
  "willingness_to_pay": "Expected budget range (e.g. $49 - $149/mo self-serve or $1k - $5k/mo contract)"
}}
"""
        response_text = self.llm.generate(system_prompt, user_prompt, response_format="json")

        parsed = {}
        try:
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            parsed = json.loads(cleaned)
        except Exception:
            from backend.agents.domain_extractor import analyze_idea_domain
            domain_info = analyze_idea_domain(raw_idea)
            parsed = {
                "icp_title": domain_info["icp_title"],
                "company_profile": {
                    "size": "5-100 team members / advisors",
                    "annual_revenue": "$500K - $10M ARR",
                    "industry": domain_info["industry"]
                },
                "acute_pain_points": domain_info["pain_points"],
                "purchasing_triggers": [
                    f"Urgent requirement to automate {domain_info['sector'].lower()} without scaling expensive headcount",
                    f"High client demand for verified {raw_idea[:40]} with strict compliance guarantees"
                ],
                "key_objections": [
                    {"objection": f"We already handle this manually or via traditional consultants.", "counter_proof": f"Cut plan delivery turnaround from weeks to minutes with zero consultant retainers."},
                    {"objection": f"Is the plan output verified or just generic AI text?", "counter_proof": "Every plan undergoes strict adversarial debate verification before delivery."}
                ],
                "willingness_to_pay": "$79 - $249/month recurring investment"
            }

        emit_thought("Demographer", f"ICP Blueprint constructed for: {parsed.get('icp_title')}.", "completed")

        return parsed
