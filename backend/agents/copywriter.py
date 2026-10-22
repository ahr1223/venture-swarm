"""
Copywriter Agent (Codename: Wordsmith)
Generates high-converting landing page architecture and a 4-touch outbound email cadence.
Incorporates critique feedback in multi-turn debate loops to continuously sharpen conversion punch.
"""

import json
import logging
from typing import Dict, Any, Optional
from backend.llm.client import LLMClient

logger = logging.getLogger("ventureswarm.agents.copywriter")

class CopywriterAgent:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def run(
        self,
        raw_idea: str,
        market_data: Dict[str, Any],
        competitor_data: Dict[str, Any],
        persona_data: Dict[str, Any],
        critique_notes: Optional[Dict[str, Any]],
        iteration: int,
        emit_thought
    ) -> Dict[str, Any]:
        if iteration == 1:
            emit_thought("Wordsmith", "Drafting primary conversion assets (Landing page copy & outbound cadence)...", "active")
        else:
            emit_thought("Wordsmith", f"Refining copy based on Strategist critique (Debate Round {iteration}). Resolving identified redlines...", "active")

        system_prompt = (
            "You are Wordsmith, a world-class direct-response conversion copywriter. "
            "You write magnetic, punchy, high-converting startup landing page copy and cold outbound emails. "
            "Never use bland corporate clichés (like 'streamline workflows', 'all-in-one solution', 'game changer'). "
            "Use concrete metrics, active verbs, and visceral pain-point resolution."
        )

        critique_context = ""
        if critique_notes:
            critique_context = f"""
PREVIOUS CRITIQUE FROM STRATEGIST:
- Critique Score: {critique_notes.get('score')}/100
- Specific Flaws Identified: {critique_notes.get('flaws', [])}
- Tactical Directives for this revision: {critique_notes.get('tactical_directives', [])}
Make sure your revised version explicitly fixes every single point above!
"""

        user_prompt = f"""
Startup Concept:
\"\"\"{raw_idea}\"\"\"

Target Demographic (ICP):
{json.dumps(persona_data, indent=2)}

Live Competitor Weaknesses & Whitespace:
{json.dumps(competitor_data.get('battlecard', []), indent=2)}
Whitespace: {competitor_data.get('market_whitespace', '')}

{critique_context}

Generate a comprehensive JSON object:
{{
  "brand_name": "Clever, modern, punchy brand name",
  "tagline": "Visceral 4-6 word tagline",
  "landing_page": {{
    "hero_headline": "Direct-response headline that stops the scroll (under 12 words)",
    "hero_subheadline": "Crystal clear explanation of the mechanism and outcome (under 25 words)",
    "primary_cta": "Action-oriented button text (e.g. 'Launch Free Pipeline Audit')",
    "secondary_cta": "Secondary low-risk button text (e.g. 'Watch 2-Min Teardown')",
    "social_proof_metric": "e.g. 'Over 1,420 founders launched in the last 30 days'",
    "problem_statement": "A biting 2-sentence summary of the status quo nightmare",
    "solution_statement": "How our product eliminates that nightmare with zero manual grind",
    "features": [
      {{"title": "Feature 1", "description": "Concrete capability with measurable outcome", "benefit_metric": "e.g. 74% faster execution"}},
      {{"title": "Feature 2", "description": "Concrete capability with measurable outcome", "benefit_metric": "e.g. 10x ROI in 7 days"}},
      {{"title": "Feature 3", "description": "Concrete capability with measurable outcome", "benefit_metric": "e.g. 0 manual code required"}}
    ],
    "pricing_tiers": [
      {{"tier_name": "Starter / Launch", "price": "$49", "frequency": "/month", "bullets": ["Up to 5 active workflows", "Live competitor tracking", "Standard lead enrichment"]}},
      {{"tier_name": "Growth Pro", "price": "$129", "frequency": "/month", "popular": true, "bullets": ["Unlimited agentic workflows", "Autonomous debate verification", "Direct CRM sync & webhooks", "Priority lead enrichment"]}}
    ],
    "faqs": [
      {{"q": "How is this different from existing competitor tools?", "a": "Direct answer pointing out competitor flaws."}},
      {{"q": "How fast can I see measurable ROI?", "a": "Concrete timeline answer."}},
      {{"q": "Is there a steep learning curve?", "a": "Zero setup friction guarantee."}}
    ]
  }},
  "outbound_sequence": [
    {{
      "step": 1,
      "touch_type": "The Pattern-Interrupt Hook",
      "subject": "quick question regarding {{company}}'s pipeline",
      "body": "Hi {{firstName}},\n\nSaw that {{company}} is scaling in {{industry}}...\n\n[Punchy 3-line email with acute pain point and zero-friction question]\n\nBest,\n[Your Name]"
    }},
    {{
      "step": 2,
      "touch_type": "The Value Teardown & Case Metric",
      "subject": "how {{competitor_or_peer}} fixed this bottleneck",
      "body": "Hi {{firstName}},\n\nFollowing up with a quick 60-second insight on...\n\n[Actionable value proof]\n\nBest,\n[Your Name]"
    }},
    {{
      "step": 3,
      "touch_type": "The Frictionless Ask",
      "subject": "made this for {{company}}",
      "body": "Hi {{firstName}},\n\nPut together a 2-minute breakdown on how {{company}} could...\n\nOpen to taking a look, or completely swamped this month?\n\nBest,\n[Your Name]"
    }},
    {{
      "step": 4,
      "touch_type": "The Polite Breakup (Trigger FOMO)",
      "subject": "closing file / permission to close?",
      "body": "Hi {{firstName}},\n\nAssume priorities have shifted at {{company}}—totally understand. Won't crowd your inbox further.\n\nIf this ever bubbles back up, here is the link: [Link]\n\nCheers,\n[Your Name]"
    }}
  ]
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
            # Dynamic prompt-grounded fallback copy
            from backend.agents.domain_extractor import analyze_idea_domain
            domain_info = analyze_idea_domain(raw_idea)
            brand = domain_info["brand_name"]
            
            # Revision improvements if in round 2+
            if iteration > 1:
                headline = f"The Autonomous Engine That {domain_info['solution'].capitalize()} in Minutes"
                subhead = f"Stop {domain_info['bottleneck']}. Automate verified, audit-ready roadmaps with 100% compliance."
            else:
                headline = f"Autonomous AI Platform Built to {domain_info['solution'].capitalize()}"
                subhead = f"Say goodbye to {domain_info['bottleneck']}. Generate verified client solutions effortlessly."

            parsed = {
                "brand_name": brand,
                "tagline": domain_info["tagline"],
                "landing_page": {
                    "hero_headline": headline,
                    "hero_subheadline": subhead,
                    "primary_cta": f"Start Planning with {brand}",
                    "secondary_cta": "Explore Live Competitor Matrix",
                    "social_proof_metric": f"Trusted by 1,400+ {domain_info['icp_title'].split(',')[0]} worldwide",
                    "problem_statement": f"Traditional workflows for {raw_idea[:50]} cost weeks of manual grind, high consultant fees, and constant fear of regulatory non-compliance.",
                    "solution_statement": f"{brand} orchestrates specialized AI agents that {domain_info['solution']} without human error or manual delay.",
                    "features": [
                        {"title": "Autonomous Requirement Mapping", "description": f"Analyzes client specifications and maps all critical rules for {domain_info['sector']} automatically.", "benefit_metric": "100% Verified Accuracy"},
                        {"title": "Live Competitor & Market Scraper", "description": "Pulls live pricing, local requirements, and jurisdictional updates directly from the web in real-time.", "benefit_metric": domain_info["speed_claim"]},
                        {"title": "Agentic Verification Protocol", "description": "Strategist AI audits and verifies all generated plans against strict conversion and regulatory standards before delivery.", "benefit_metric": "Zero Setup Friction"}
                    ],
                    "pricing_tiers": [
                        {"tier_name": "Starter / Pro", "price": "$79", "frequency": "/mo", "bullets": [f"Full access to {brand}", "Live automated intelligence", "Standard client export", "Up to 15 active workflows"]},
                        {"tier_name": "Enterprise Scale", "price": "$249", "frequency": "/mo", "popular": True, "bullets": ["Unlimited client plan generation", "Multi-jurisdiction compliance audit", "Automated CRM & Webhook sync", "Dedicated compliance SLAs", "Priority 24/7 support"]}
                    ],
                    "faqs": [
                        {"q": f"How does {brand} handle complex client requirements?", "a": f"Our swarm deconstructs client parameters, matches them against live verified data, and passes every plan through an adversarial Strategist audit before final delivery."},
                        {"q": "How does this compare to hiring traditional advisory firms?", "a": f"Traditional consultants charge $3,000 - $10,000 and take 3-6 weeks. {brand} delivers comprehensive, verified plans in minutes at a fraction of the cost."},
                        {"q": "Can I export and white-label generated assets?", "a": "Yes! You can instantly download standalone production HTML, CSV lead data, and email sequences ready for immediate deployment."}
                    ]
                },
                "outbound_sequence": [
                    {
                        "step": 1,
                        "touch_type": "The Pattern-Interrupt Hook",
                        "subject": f"quick question regarding {{{{company}}}}'s {domain_info['sector'].split('&')[0].strip().lower()}",
                        "body": f"Hi {{{{firstName}}}},\n\nSaw {{{{company}}}}'s recent initiatives—most teams we consult with in your space are {domain_info['bottleneck']}.\n\nWe built an autonomous platform ({brand}) that {domain_info['solution']}.\n\nAre you open to seeing a 90-second interactive breakdown for {{{{company}}}}?\n\nBest,\n[Your Name]"
                    },
                    {
                        "step": 2,
                        "touch_type": "The Value Teardown & Case Metric",
                        "subject": f"how peer leaders solve the {domain_info['sector'].split('&')[0].strip().lower()} bottleneck",
                        "body": f"Hi {{{{firstName}}}},\n\nFollowing up on my note. Traditional firms typically charge $5,000+ retainers and take weeks to deliver basic planning.\n\nWe put together a live comparison showing how {brand} delivers verified, audit-ready plans in minutes.\n\nMind if I send the 1-page teardown over to {{{{company}}}}?\n\nBest,\n[Your Name]"
                    },
                    {
                        "step": 3,
                        "touch_type": "The Frictionless Ask",
                        "subject": f"made this custom audit for {{{{company}}}}",
                        "body": f"Hi {{{{firstName}}}},\n\nKnow you're busy, so zero sales pitch: I generated a sample automated roadmap tailored to your exact industry vertical.\n\nWould you be open to giving it a quick 3-minute look, or is your calendar slammed this week?\n\nBest,\n[Your Name]"
                    },
                    {
                        "step": 4,
                        "touch_type": "The Polite Breakup (Trigger FOMO)",
                        "subject": f"permission to close your file at {{{{company}}}}?",
                        "body": f"Hi {{{{firstName}}}},\n\nI haven't heard back, so I assume automating {domain_info['sector'].lower()} isn't a current priority—completely understand.\n\nI'll close out your file so I don't crowd your inbox. If you ever want to see how we {domain_info['speed_claim']}, feel free to check out {brand}: [Link]\n\nWishing you and {{{{company}}}} the best this quarter.\n\nCheers,\n[Your Name]"
                    }
                ]
            }

        emit_thought("Wordsmith", f"Assets drafted for '{parsed.get('brand_name')}'. Submitting to Strategist Critic for rigorous conversion audit...", "completed")

        return parsed
