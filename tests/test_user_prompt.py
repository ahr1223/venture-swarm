"""
Test user prompt alignment for: 'AI Agent that helps client with international plans'
"""

import sys
import os
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.orchestrator import SwarmOrchestrator

async def main():
    prompt = "AI Agent that helps client with international plans"
    print(f"\n--- Testing User Prompt: '{prompt}' ---")
    orch = SwarmOrchestrator(max_debate_rounds=2)

    async for event in orch.run_swarm_stream(prompt):
        etype = event.get("type")
        if etype == "thought" and event.get("status") in ["critique", "approved"]:
            print(f"\n[{event['agent']}] ({event['status']}): {event['message']}")
            d = event.get("payload", {}).get("debate_entry")
            if d:
                print(f"  Round #{d.get('round')}: {d.get('verdict')} (Score: {d.get('score')}/100)")
                print(f"  Flaws: {d.get('flaws')}")
                print(f"  Directives: {d.get('directives')}")
        elif etype == "done":
            assets = event.get("final_assets")
            print("\n[SUCCESS - FINAL ASSETS VERIFICATION]")
            print(f"Brand: {assets.get('brand_name')}")
            print(f"Tagline: {assets.get('tagline')}")
            print(f"Hero Headline: {assets.get('landing_page_data', {}).get('hero_headline')}")
            print(f"Features: {[f['title'] for f in assets.get('landing_page_data', {}).get('features', [])]}")
            print(f"Lead Titles: {[line.split(',')[2] for line in assets.get('leads_csv', '').splitlines()[1:4]]}")
            print(f"Final Score: {assets.get('final_score')}/100")

if __name__ == "__main__":
    asyncio.run(main())
