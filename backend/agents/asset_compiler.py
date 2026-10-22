"""
Asset Compiler & Synthesis Agent (Codename: Foundry)
Produces tangible, deployable business revenue assets:
1. High-converting responsive Tailwind CSS Landing Page (index.html)
2. Simulated high-intent ICP Lead List (leads.csv)
3. Structured Outbound Email Sequence Cadence
4. Competitor Positioning Battlecard
"""

import csv
import io
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger("ventureswarm.agents.foundry")

class AssetCompilerAgent:
    def __init__(self):
        pass

    def generate_landing_page_html(
        self,
        brand_name: str,
        tagline: str,
        landing_page_data: Dict[str, Any],
        competitor_battlecard: List[Dict[str, Any]]
    ) -> str:
        """
        Builds a high-impact, standalone responsive landing page using Tailwind CSS.
        """
        hero_headline = landing_page_data.get("hero_headline", f"Autonomous Revenue Engine for {brand_name}")
        hero_subheadline = landing_page_data.get("hero_subheadline", "Deploy verified landing pages, competitor teardowns, and outbound sequences in minutes.")
        primary_cta = landing_page_data.get("primary_cta", "Start Free Trial")
        secondary_cta = landing_page_data.get("secondary_cta", "See Live Demo")
        social_proof = landing_page_data.get("social_proof_metric", "Over 1,200+ companies launched this month")
        problem = landing_page_data.get("problem_statement", "Manual go-to-market workflows cost weeks of lost revenue and high consultant fees.")
        solution = landing_page_data.get("solution_statement", "Our autonomous agent swarm executes market research, competitor teardown, and copy in under 10 minutes.")

        features = landing_page_data.get("features", [])
        pricing_tiers = landing_page_data.get("pricing_tiers", [])
        faqs = landing_page_data.get("faqs", [])

        # Build feature cards HTML
        feature_cards_html = ""
        for i, f in enumerate(features[:3]):
            icon_svg = [
                '<svg class="w-6 h-6 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>',
                '<svg class="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>',
                '<svg class="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2 1.5 3 3.5 3h9c2 0 3.5-1 3.5-3V7c0-2-1.5-3-3.5-3h-9C5.5 4 4 5 4 7zm0 4h16"/></svg>'
            ][i % 3]

            feature_cards_html += f"""
            <div class="bg-[#161b22] border border-[#30363d] p-8 rounded-xl hover:border-[#58a6ff]/50 transition">
              <div class="w-12 h-12 rounded-lg bg-[#21262d] border border-[#30363d] flex items-center justify-center mb-6 text-[#58a6ff]">
                {icon_svg}
              </div>
              <div class="inline-block px-2.5 py-1 text-xs font-mono font-medium rounded-full bg-[#21262d] text-[#58a6ff] mb-3 border border-[#30363d]">
                {f.get('benefit_metric', 'High Impact')}
              </div>
              <h3 class="text-xl font-bold text-[#f0f6fc] mb-2">{f.get('title', 'Intelligent Automation')}</h3>
              <p class="text-[#8b949e] text-sm leading-relaxed">{f.get('description', '')}</p>
            </div>
            """

        # Build pricing cards HTML
        pricing_cards_html = ""
        for p in pricing_tiers:
            is_popular = p.get("popular", False)
            border_cls = "border-[#238636] shadow-lg shadow-[#238636]/10" if is_popular else "border-[#30363d]"
            badge = '<div class="absolute -top-3 right-6 px-3 py-0.5 text-xs font-bold rounded-full bg-[#238636] text-white uppercase tracking-wider">Most Popular</div>' if is_popular else ""
            
            bullets_html = ""
            for b in p.get("bullets", []):
                bullets_html += f"""
                <li class="flex items-center text-sm text-[#c9d1d9]">
                  <svg class="w-4 h-4 text-[#3fb950] mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                  {b}
                </li>
                """

            pricing_cards_html += f"""
            <div class="relative bg-[#161b22] border {border_cls} rounded-2xl p-8 flex flex-col justify-between">
              {badge}
              <div>
                <h4 class="text-lg font-bold text-[#f0f6fc] mb-1">{p.get('tier_name', 'Plan')}</h4>
                <div class="flex items-baseline gap-1 my-4">
                  <span class="text-4xl font-extrabold text-[#f0f6fc]">{p.get('price', '$49')}</span>
                  <span class="text-[#8b949e] text-sm">{p.get('frequency', '/mo')}</span>
                </div>
                <ul class="space-y-3 mb-8">
                  {bullets_html}
                </ul>
              </div>
              <button onclick="alert('Demo Lead Captured! In production, this opens your Stripe checkout.')" class="w-full py-3 px-4 rounded-lg font-semibold text-sm transition {'bg-[#238636] hover:bg-[#2ea043] text-white font-bold' if is_popular else 'bg-[#21262d] hover:bg-[#30363d] text-[#c9d1d9] border border-[#30363d]'}">
                Get Started
              </button>
            </div>
            """

        # Build competitor comparison rows
        comp_rows_html = ""
        for c in competitor_battlecard[:3]:
            comp_rows_html += f"""
            <tr class="border-b border-[#30363d] hover:bg-[#21262d]/50">
              <td class="py-4 px-6 font-semibold text-[#f0f6fc]">{c.get('name', 'Incumbent')}</td>
              <td class="py-4 px-6 text-[#8b949e] font-mono text-xs">{c.get('pricing_model', 'Seats')}</td>
              <td class="py-4 px-6 text-[#f85149] text-sm">{c.get('critical_weakness', 'High manual friction')}</td>
              <td class="py-4 px-6 text-[#3fb950] font-medium text-sm">{c.get('our_counter_attack', 'Autonomous execution')}</td>
            </tr>
            """

        # Build FAQ HTML
        faq_html = ""
        for faq in faqs:
            faq_html += f"""
            <div class="border border-[#30363d] rounded-xl p-6 bg-[#161b22]">
              <h4 class="text-base font-bold text-[#f0f6fc] mb-2">{faq.get('q', 'Question')}</h4>
              <p class="text-sm text-[#8b949e] leading-relaxed">{faq.get('a', 'Answer')}</p>
            </div>
            """

        html_template = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{brand_name} — {tagline}</title>
  <meta name="description" content="{hero_subheadline}">
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    html, body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #0d1117 !important;
      color: #f0f6fc !important;
      margin: 0;
      padding: 0;
    }}
    .font-mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    .hero-glow {{
      background-color: #0d1117;
      background-image: radial-gradient(circle at 50% 15%, rgba(56, 139, 253, 0.12) 0%, rgba(13, 17, 23, 1) 70%);
    }}
  </style>
</head>
<body class="min-h-screen bg-[#0d1117] text-[#f0f6fc] hero-glow selection:bg-[#238636] selection:text-white">

  <!-- Navbar -->
  <header class="sticky top-0 z-50 backdrop-blur-md bg-[#161b22]/90 border-b border-[#30363d]">
    <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 rounded-lg bg-amber-500 flex items-center justify-center font-extrabold text-black text-base">
          {brand_name[0] if brand_name else 'V'}
        </div>
        <span class="font-extrabold text-lg tracking-tight text-white">{brand_name}</span>
      </div>
      <div class="hidden md:flex items-center space-x-8 text-sm text-neutral-400 font-medium">
        <a href="#features" class="hover:text-white transition">Capabilities</a>
        <a href="#matrix" class="hover:text-white transition">Versus Incumbents</a>
        <a href="#pricing" class="hover:text-white transition">Pricing</a>
        <a href="#faq" class="hover:text-white transition">FAQ</a>
      </div>
      <div class="flex items-center space-x-3">
        <button onclick="document.getElementById('cta-modal').classList.remove('hidden')" class="px-4 py-2 text-xs font-bold uppercase tracking-wider bg-amber-500 hover:bg-amber-400 text-black rounded-lg transition shadow-sm">
          {primary_cta}
        </button>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="pt-24 pb-20 px-6 max-w-5xl mx-auto text-center">
    <div class="inline-flex items-center space-x-2 px-3 py-1.5 rounded-full border border-neutral-700/80 bg-neutral-900/80 text-xs text-neutral-300 font-mono mb-8">
      <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
      <span>Autonomous Swarm Engine Activated</span>
      <span class="text-neutral-500">•</span>
      <span class="text-amber-400">{social_proof}</span>
    </div>

    <h1 class="text-4xl sm:text-6xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-tight mb-6">
      {hero_headline}
    </h1>

    <p class="text-lg sm:text-xl text-neutral-400 max-w-2xl mx-auto mb-10 leading-relaxed">
      {hero_subheadline}
    </p>

    <div class="flex flex-col sm:flex-row items-center justify-center gap-4 max-w-md mx-auto mb-16">
      <button onclick="document.getElementById('cta-modal').classList.remove('hidden')" class="w-full sm:w-auto px-8 py-3.5 rounded-lg text-white font-bold text-sm bg-[#238636] hover:bg-[#2ea043] border border-[#3fb950]/30 transition shadow-sm">
        {primary_cta}
      </button>
      <a href="#matrix" class="w-full sm:w-auto px-8 py-3.5 rounded-lg text-[#c9d1d9] font-medium text-sm bg-[#21262d] hover:bg-[#30363d] border border-[#30363d] transition text-center">
        {secondary_cta}
      </a>
    </div>

    <!-- Status quo vs Modern Solution -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-left max-w-4xl mx-auto pt-6 border-t border-[#30363d]">
      <div class="p-6 rounded-xl bg-[#da3633]/10 border border-[#f85149]/30">
        <div class="text-xs font-mono font-bold text-[#f85149] uppercase tracking-widest mb-2">The Old Way (Manual Burn)</div>
        <p class="text-[#c9d1d9] text-sm leading-relaxed">{problem}</p>
      </div>
      <div class="p-6 rounded-xl bg-[#238636]/10 border border-[#3fb950]/30">
        <div class="text-xs font-mono font-bold text-[#3fb950] uppercase tracking-widest mb-2">The {brand_name} Way (Autonomous)</div>
        <p class="text-[#c9d1d9] text-sm leading-relaxed">{solution}</p>
      </div>
    </div>
  </section>

  <!-- Feature Pillars -->
  <section id="features" class="py-20 px-6 max-w-6xl mx-auto">
    <div class="text-center max-w-2xl mx-auto mb-16">
      <h2 class="text-xs font-mono uppercase tracking-widest text-[#58a6ff] font-bold mb-3">Core Pillars</h2>
      <p class="text-3xl font-extrabold text-[#f0f6fc]">Built for immediate execution and revenue capture.</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      {feature_cards_html}
    </div>
  </section>

  <!-- Competitor Comparison Matrix -->
  <section id="matrix" class="py-20 px-6 max-w-6xl mx-auto">
    <div class="text-center max-w-2xl mx-auto mb-12">
      <h2 class="text-xs font-mono uppercase tracking-widest text-[#58a6ff] font-bold mb-3">Live Market Teardown</h2>
      <p class="text-3xl font-extrabold text-[#f0f6fc]">Why our model out-executes legacy alternatives.</p>
    </div>
    <div class="overflow-x-auto rounded-xl border border-[#30363d] bg-[#161b22]">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="border-b border-[#30363d] bg-[#0d1117] text-xs font-mono text-[#8b949e] uppercase">
            <th class="py-4 px-6">Competitor Entity</th>
            <th class="py-4 px-6">Pricing Model</th>
            <th class="py-4 px-6">Critical Bottleneck</th>
            <th class="py-4 px-6">Our Distinct Advantage</th>
          </tr>
        </thead>
        <tbody>
          {comp_rows_html if comp_rows_html else '<tr><td colspan="4" class="p-6 text-center text-[#8b949e]">Competitive intelligence populated via live scraper</td></tr>'}
        </tbody>
      </table>
    </div>
  </section>

  <!-- Pricing Section -->
  <section id="pricing" class="py-20 px-6 max-w-5xl mx-auto">
    <div class="text-center max-w-2xl mx-auto mb-16">
      <h2 class="text-xs font-mono uppercase tracking-widest text-[#58a6ff] font-bold mb-3">Predictable Investment</h2>
      <p class="text-3xl font-extrabold text-[#f0f6fc]">Outcome-driven pricing. No per-seat extortion.</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-3xl mx-auto">
      {pricing_cards_html}
    </div>
  </section>

  <!-- FAQ Section -->
  <section id="faq" class="py-20 px-6 max-w-3xl mx-auto">
    <div class="text-center mb-12">
      <h2 class="text-xs font-mono uppercase tracking-widest text-[#58a6ff] font-bold mb-3">Questions & Verification</h2>
      <p class="text-3xl font-extrabold text-[#f0f6fc]">Frequently Asked Questions</p>
    </div>
    <div class="space-y-4">
      {faq_html}
    </div>
  </section>

  <!-- Final CTA Bar -->
  <section class="py-20 px-6 max-w-5xl mx-auto text-center border-t border-[#30363d]">
    <div class="bg-[#161b22] border border-[#30363d] p-12 rounded-2xl">
      <h2 class="text-3xl sm:text-4xl font-extrabold text-[#f0f6fc] mb-4">Ready to launch {brand_name}?</h2>
      <p class="text-[#8b949e] max-w-xl mx-auto mb-8 text-sm sm:text-base">Join high-velocity teams capturing revenue while competitors are still stuck in planning meetings.</p>
      <button onclick="document.getElementById('cta-modal').classList.remove('hidden')" class="px-8 py-4 rounded-lg text-white font-bold text-base bg-[#238636] hover:bg-[#2ea043] border border-[#3fb950]/30 transition shadow-md">
        {primary_cta} Now
      </button>
    </div>
  </section>

  <!-- Lead Capture Modal -->
  <div id="cta-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
    <div class="bg-[#161b22] border border-[#30363d] p-8 rounded-2xl max-w-md w-full relative shadow-2xl">
      <button onclick="document.getElementById('cta-modal').classList.add('hidden')" class="absolute top-4 right-4 text-[#8b949e] hover:text-[#f0f6fc]">✕</button>
      <h3 class="text-xl font-bold text-[#f0f6fc] mb-2">Claim Early Access to {brand_name}</h3>
      <p class="text-sm text-[#8b949e] mb-6">Enter your email to test-drive the live autonomous revenue engine.</p>
      <form onsubmit="event.preventDefault(); alert('Lead saved! In production, this syncs directly with your CRM or email provider.'); document.getElementById('cta-modal').classList.add('hidden');" class="space-y-4">
        <div>
          <label class="block text-xs font-mono text-[#8b949e] mb-1">WORK EMAIL</label>
          <input type="email" required placeholder="founder@company.com" class="w-full px-4 py-3 rounded-lg bg-[#0d1117] border border-[#30363d] text-[#f0f6fc] placeholder-[#6e7681] focus:outline-none focus:border-[#58a6ff] text-sm">
        </div>
        <button type="submit" class="w-full py-3 px-4 rounded-lg font-bold text-white bg-[#238636] hover:bg-[#2ea043] border border-[#3fb950]/30 transition">
          Instant Launch Access →
        </button>
      </form>
    </div>
  </div>

  <!-- Footer -->
  <footer class="py-8 border-t border-[#21262d] text-center text-xs text-[#8b949e] font-mono">
    Generated autonomously by VentureSwarm Multi-Agent Architecture.
  </footer>
</body>
</html>
"""
        return html_template

    def generate_leads_csv(self, brand_name: str, persona_data: Dict[str, Any]) -> str:
        """
        Synthesizes a realistic, high-intent B2B prospect CSV matching the ICP.
        """
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "First Name",
            "Last Name",
            "Title",
            "Company",
            "Company Domain",
            "Employees",
            "Estimated Tech Budget",
            "Cold Hook Personalization Angle",
            "Email Address",
            "LinkedIn Search Query"
        ])

        icp_role = persona_data.get("icp_title", "Director of Operations")
        industry = persona_data.get("company_profile", {}).get("industry", "Global Advisory")
        pain_samples = persona_data.get("acute_pain_points", ["manual workflow bottlenecks", "costly consultant overhead"])

        titles = [
            icp_role,
            f"VP of {industry.split('&')[0].strip()}",
            "Managing Director",
            f"Head of Client Services ({industry.split('&')[0].strip()})",
            "Chief Commercial Officer",
            "Partner & Principal Advisor",
            f"Senior Director of {industry.split('&')[0].strip()}",
            "Head of Strategic Operations"
        ]

        companies = [
            ("Atlas Global Advisory", "atlasglobal.co", "25-75", "$6,000/mo", f"Eliminating {pain_samples[0] if pain_samples else 'manual bottlenecks'}"),
            ("Vanguard International Partners", "vanguardintl.com", "50-150", "$12,000/mo", f"Automating client plans without adding headcount"),
            ("Meridian Cross-Border Group", "meridianborders.io", "15-45", "$4,500/mo", f"Reducing turnaround time from 3 weeks to 10 minutes"),
            ("Starlight Commercial Advisory", "starlightadvisory.tech", "30-100", "$8,500/mo", f"Cutting advisory preparation costs by 70%"),
            ("Crestview Global Solutions", "crestviewintl.io", "20-60", "$5,000/mo", f"Replacing disjointed manual research with verified automation"),
            ("Nexus Prime Advisors", "nexusprime.co", "10-35", "$3,500/mo", f"Streamlining complex multi-region client deliverables"),
            ("Kinetics Global Enterprise", "kineticsgroup.co", "40-120", "$9,000/mo", f"Zero-error verification across all client workflows"),
            ("Beacon Mobility & Strategy", "beaconmobility.io", "15-50", "$5,500/mo", f"Instant compliance checks and live roadmaps on demand")
        ]

        first_names = ["Marcus", "Elena", "Devon", "Sophia", "Julian", "Aria", "Tariq", "Chloe"]
        last_names = ["Vance", "Kovacs", "Sterling", "Chen", "Mercer", "Lindqvist", "Farhan", "Duval"]

        for i in range(len(companies)):
            fn = first_names[i % len(first_names)]
            ln = last_names[i % len(last_names)]
            c_name, domain, size, budget, hook = companies[i]
            title = titles[i % len(titles)]
            email = f"{fn.lower()}.{ln.lower()}@{domain}"
            linkedin_q = f"https://www.linkedin.com/search/results/people/?keywords={fn}+{ln}+{c_name}"

            writer.writerow([
                fn, ln, title, c_name, domain, size, budget, hook, email, linkedin_q
            ])

        return output.getvalue()
