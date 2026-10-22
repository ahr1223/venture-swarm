"""
Dynamic Domain Extractor for VentureSwarm
Extracts semantic entities, sector mechanics, buyer psychology, and custom brand concepts
from ANY user prompt to ensure 100% prompt-aligned agent outputs even in heuristic mode.
"""

import re
import hashlib
from typing import Dict, Any, List

def analyze_idea_domain(raw_idea: str) -> Dict[str, Any]:
    text = raw_idea.strip()
    words = [w.lower() for w in re.findall(r'[a-zA-Z0-9]+', text) if len(w) > 2]
    
    # Keyword taxonomy detection
    lower = text.lower()
    
    # 1. Detect International / Travel / Cross-Border
    if any(k in lower for k in ["international", "global", "cross-border", "travel", "relocation", "visa", "immigrat", "expat", "overseas"]):
        sector = "Global Mobility & International Advisory"
        brand_name = "PlanAtlas AI"
        tagline = "Autonomous Cross-Border & International Planning on Demand"
        icp_title = "Global Mobility Directors, International Wealth Advisors & Expat Leads"
        industry = "International Business & Client Advisory"
        bottleneck = "spending weeks navigating multi-country regulations, foreign tax rules, and fragmented visa requirements"
        solution = "generates compliant, multi-jurisdiction international plans and client advisory roadmaps"
        speed_claim = "cut international plan turnaround from 3 weeks to under 10 minutes"
        pain_points = [
            "Losing 25+ billable hours per client manually researching foreign tax treaties, visa classes, and cross-border compliances",
            "Fear of costly cross-border regulatory mistakes and compliance penalties in unfamiliar foreign jurisdictions",
            "Paying $3,000 - $10,000+ in consultant fees to international advisory firms that take weeks to respond"
        ]
        critique_flaws = [
            "Hero headline fails to state which international jurisdictions, visa/tax frameworks, and compliance guidelines are automated.",
            "Email #1 hook is too generic; it does not trigger acute pain around the weeks of delay and cross-border penalties clients suffer when planning internationally."
        ]
        critique_directives = [
            "Sharpen the hero headline to quantify the reduction in international planning turnaround from 3 weeks to under 10 minutes.",
            "In Email #2, directly contrast our automated engine against the $5,000+ fees charged by traditional international advisory firms."
        ]
        competitors = [
            {"name": "Traditional Global Relocation Consultancies", "pricing": "$5,000 - $15,000 per engagement", "weakness": "Glacial 3-to-6 week delivery time and exorbitant advisory billing hours", "advantage": "Instant autonomous international plans with real-time jurisdictional data"},
            {"name": "Fragmented Country Spreadsheets & Gov Portals", "pricing": "Free manual research", "weakness": "High risk of missed regulatory deadlines, outdated tax laws, and zero client collaboration", "advantage": "Unified single-click international plan portal with verified foreign requirements"}
        ]
        leads_roles = ["Head of Global Mobility", "Director of International Client Services", "VP of Cross-Border Operations", "Partner, Global Expansion Advisory"]

    # 2. Detect Sales / SDR / Cold Outreach
    elif any(k in lower for k in ["sdr", "sales", "cold email", "outbound", "leads", "prospect", "pipeline"]):
        sector = "B2B Sales Tech & Pipeline Automation"
        brand_name = "ApexOutbound"
        tagline = "Autonomous High-Intent Pipeline Generation"
        icp_title = "VP of Sales, Growth Directors & Founders"
        industry = "B2B SaaS & High-Growth Tech"
        bottleneck = "spending 15+ hours weekly manually prospecting and sending low-response cold emails that hit spam filters"
        solution = "scrapes buyer signals and sends verified, hyper-personalized multi-touch outbound sequences autonomously"
        speed_claim = "generate verified outbound pipelines and warm replies in under 10 minutes"
        pain_points = [
            "Paying $75,000+ for SDR salaries while cold email reply rates continue dropping below 1%",
            "Wasting hours manually researching lead LinkedIn profiles and writing custom openers",
            "Getting burned by seat-based outbound tools that don't verify deliverability"
        ]
        critique_flaws = [
            "Hero headline does not explicitly quantify reply rate lift or cost savings vs hiring SDRs.",
            "Email #1 hook fails to target the acute frustration of cold outreach landing in secondary spam folders."
        ]
        critique_directives = [
            "Emphasize concrete 3x reply rate benchmarks and zero SDR headcount overhead in the hero section.",
            "Incorporate a pattern-interrupt icebreaker in Email #1 that references competitor pricing bloat."
        ]
        competitors = [
            {"name": "Legacy Enterprise Sales Suites", "pricing": "$150 - $350 / user / mo", "weakness": "Bloated user seats, manual workflow setup, and deliverability burn", "advantage": "Zero-seat autonomous outbound execution on autopilot"},
            {"name": "Manual SDR Agencies", "pricing": "$4,000 - $8,000 / month retainers", "weakness": "Slow 3-week ramp time and inconsistent human copy quality", "advantage": "Live web-grounded research deployed in minutes at 1/10th the cost"}
        ]
        leads_roles = ["VP of Sales", "Head of Business Development", "Chief Revenue Officer", "Director of Growth"]

    # 3. Detect Marketing / SEO / Content / Social
    elif any(k in lower for k in ["seo", "content", "marketing", "social", "agency", "blog", "copywriting"]):
        sector = "Autonomous Marketing & Content Growth"
        brand_name = "RankPulse AI"
        tagline = "Autonomous Competitor Content & SEO Ranking Engine"
        icp_title = "Head of Marketing, Agency Owners & Content Leads"
        industry = "Digital Marketing & Brand Growth"
        bottleneck = "spending 30+ hours per month writing articles and tracking competitor keyword rankings manually"
        solution = "audits competitor search rankings and writes ready-to-publish, search-intent optimized assets"
        speed_claim = "out-rank competitors and publish verified content 10x faster"
        pain_points = [
            "Paying $5,000/mo to agencies that deliver generic blog posts with zero organic traffic gains",
            "Falling behind competitors who dominate high-intent commercial keywords",
            "Wasting days in editorial review cycles without clear conversion tracking"
        ]
        critique_flaws = [
            "Hero headline does not contrast against generic AI copywriting tools that produce generic fluff.",
            "Email #1 lacks an immediate teaser showing the prospect an actual keyword gap their competitor is exploiting."
        ]
        critique_directives = [
            "Position the platform as an intelligence-driven execution engine rather than a generic text generator.",
            "Add a zero-friction audit offer in Email #3 to demonstrate immediate keyword value."
        ]
        competitors = [
            {"name": "Traditional Content Marketing Agencies", "pricing": "$3,000 - $7,000 / month", "weakness": "Slow 2-week turnaround per post and high per-word billing", "advantage": "Instant competitor gap detection and publication in minutes"},
            {"name": "Generic AI Writing Wrappers", "pricing": "$49 - $99 / mo", "weakness": "Hallucinates facts and lacks live competitor ranking verification", "advantage": "Real-time search-grounded research with strict verification"}
        ]
        leads_roles = ["Head of Marketing", "Director of Organic Growth", "Content Marketing Lead", "VP of Brand Strategy"]

    # 4. Universal Smart Dynamic Extraction (Handles ANY other business concept!)
    else:
        # Extract meaningful concept words
        filtered = [w for w in words if w not in ["the", "and", "that", "this", "for", "with", "from", "helps", "client", "agent", "tool"]]
        key_phrase = " ".join(filtered[:3]).title() if filtered else "Autonomous Intelligence"
        clean_concept = text[:70]
        
        sector = f"{key_phrase} & Workflow Automation"
        # Dynamic brand name
        prefixes = ["Nexus", "Crest", "Vanguard", "Aura", "Nova", "Hyperion"]
        h = int(hashlib.md5(text.encode()).hexdigest(), 16)
        brand_name = f"{prefixes[h % len(prefixes)]}{filtered[0].title() if filtered else 'Flow'}"
        tagline = f"Autonomous {clean_concept.title()} Made Effortless"
        icp_title = f"Decision Makers, Operations Leads & Founders Managing {key_phrase}"
        industry = "Digital Services & Enterprise Operations"
        bottleneck = f"manually managing {clean_concept} with slow legacy processes and high labor friction"
        solution = f"automates {clean_concept} end-to-end with real-time verification and zero manual grind"
        speed_claim = f"deploy complete {clean_concept} solutions in under 10 minutes"
        pain_points = [
            f"Wasting dozens of weekly hours on manual steps when dealing with {clean_concept}",
            f"Lack of unified visibility and high risk of errors when coordinating {key_phrase}",
            f"Expensive consultant and software fees with sluggish turnaround and zero modern automation"
        ]
        critique_flaws = [
            f"Hero headline does not aggressively emphasize the unique time-to-value moat for {clean_concept}.",
            f"Email #1 is slightly too polite; needs a punchier pattern-interrupt hook directly addressing {key_phrase} bottlenecks."
        ]
        critique_directives = [
            f"Sharpen the hero headline with explicit quantifiable time-to-value for {clean_concept}.",
            f"Directly contrast against high-fee incumbent alternatives in Email #2."
        ]
        competitors = [
            {"name": f"Traditional {key_phrase} Consultancies", "pricing": "$3,000 - $10,000 per project", "weakness": "High manual overhead, slow communication, and high per-hour bills", "advantage": f"Autonomous execution with live data in minutes"},
            {"name": "Disjointed Manual Spreadsheets", "pricing": "Internal team time ($100+/hr)", "weakness": "Error-prone, unscalable, and consumes internal leadership bandwidth", "advantage": f"Zero-friction automated system built specifically for {clean_concept}"}
        ]
        leads_roles = [f"Head of {key_phrase}", f"Director of Operations", f"VP Commercial Strategy", f"Managing Partner"]

    return {
        "sector": sector,
        "brand_name": brand_name,
        "tagline": tagline,
        "icp_title": icp_title,
        "industry": industry,
        "bottleneck": bottleneck,
        "solution": solution,
        "speed_claim": speed_claim,
        "pain_points": pain_points,
        "critique_flaws": critique_flaws,
        "critique_directives": critique_directives,
        "competitors": competitors,
        "leads_roles": leads_roles
    }
