"""
Verification test for VentureSwarm Orchestrator
"""

import sys
import os
import asyncio

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.orchestrator import SwarmOrchestrator

async def run_test():
    print("\n--- Starting VentureSwarm Verification Test ---")
    orchestrator = SwarmOrchestrator(max_debate_rounds=1)
    sample_idea = "AI copilot for B2B outbound sales that scrapes competitor reviews"
    
    event_count = 0
    final_assets = None

    async for event in orchestrator.run_swarm_stream(sample_idea):
        event_count += 1
        event_type = event.get("type")
        if event_type == "thought":
            agent = event.get("agent")
            status = event.get("status")
            msg = event.get("message")
            print(f"[{event['timestamp']}s] [{agent}] ({status}): {msg[:80]}")
        elif event_type == "done":
            final_assets = event.get("final_assets")
            print("\n[SUCCESS] Final Assets Received!")
            print(f"Brand: {final_assets.get('brand_name')}")
            print(f"Tagline: {final_assets.get('tagline')}")
            print(f"Landing Page HTML bytes: {len(final_assets.get('landing_page_html', ''))}")
            print(f"Leads CSV lines: {len(final_assets.get('leads_csv', '').splitlines())}")
            print(f"Emails in cadence: {len(final_assets.get('outbound_sequence', []))}")
            print(f"Debate Score: {final_assets.get('final_score')}/100")

    assert final_assets is not None, "Final assets were not generated!"
    print(f"\n--- Test Passed with {event_count} streamed events! ---\n")

if __name__ == "__main__":
    asyncio.run(run_test())
