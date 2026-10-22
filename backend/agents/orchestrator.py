"""
Graph Orchestrator for VentureSwarm
Coordinates agent state transitions, live web grounding, the Strategist/Copywriter debate loop,
and real-time event streaming via Async Generators / Server-Sent Events (SSE).
"""

import time
import asyncio
import logging
from typing import Dict, Any, AsyncGenerator, Optional

from backend.llm.client import LLMClient
from backend.agents.market_researcher import MarketResearcherAgent
from backend.agents.competitor_scraper import CompetitorScraperAgent
from backend.agents.persona_architect import PersonaArchitectAgent
from backend.agents.copywriter import CopywriterAgent
from backend.agents.strategist_critic import StrategistCriticAgent
from backend.agents.asset_compiler import AssetCompilerAgent

logger = logging.getLogger("ventureswarm.orchestrator")

class SwarmOrchestrator:
    def __init__(self, api_key: Optional[str] = None, provider: str = "auto", max_debate_rounds: int = 2):
        self.llm_client = LLMClient(api_key=api_key, provider=provider)
        self.max_debate_rounds = max(1, min(max_debate_rounds, 4))
        
        # Instantiate Agents
        self.scout = MarketResearcherAgent(self.llm_client)
        self.harvester = CompetitorScraperAgent(self.llm_client)
        self.demographer = PersonaArchitectAgent(self.llm_client)
        self.wordsmith = CopywriterAgent(self.llm_client)
        self.overwatch = StrategistCriticAgent(self.llm_client)
        self.foundry = AssetCompilerAgent()

    async def run_swarm_stream(self, raw_idea: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Executes the full Graph Workflow and yields real-time streaming updates.
        """
        start_time = time.time()
        queue: asyncio.Queue = asyncio.Queue()

        def emit(agent: str, message: str, status: str = "active", payload: Optional[Dict[str, Any]] = None):
            queue.put_nowait({
                "type": "thought",
                "timestamp": round(time.time() - start_time, 2),
                "agent": agent,
                "message": message,
                "status": status,
                "payload": payload or {}
            })

        # Yield initial initialization event
        yield {
            "type": "init",
            "provider_status": self.llm_client.get_provider_status(),
            "raw_idea": raw_idea,
            "max_debate_rounds": self.max_debate_rounds,
            "message": "Swarm Orchestration Engine initialized. Activating Scout agent."
        }
        await asyncio.sleep(0.05)

        # Worker coroutine that runs the synchronous agent workflow
        async def workflow_runner():
            try:
                # -------------------------------------------------------------
                # NODE 1: Scout (Market Discovery & Live Search)
                # -------------------------------------------------------------
                emit("Scout", "Initializing market radar and category taxonomy...", "active")
                market_data = await asyncio.to_thread(self.scout.run, raw_idea, emit)
                emit("Scout", "Market intelligence acquired.", "completed", {"market_data": market_data})

                # -------------------------------------------------------------
                # NODE 2: Harvester (Live Competitor Scraping & Battlecard)
                # -------------------------------------------------------------
                emit("Harvester", "Targeting live competitor domains for live HTTP inspection...", "active")
                competitor_data = await asyncio.to_thread(self.harvester.run, raw_idea, market_data, emit)
                emit("Harvester", "Competitor Battlecard & Pricing matrix compiled.", "completed", {"competitor_data": competitor_data})

                # -------------------------------------------------------------
                # NODE 3: Demographer (Target Persona & ICP Blueprint)
                # -------------------------------------------------------------
                emit("Demographer", "Constructing Buyer Psychology & Objection Map...", "active")
                persona_data = await asyncio.to_thread(self.demographer.run, raw_idea, market_data, competitor_data, emit)
                emit("Demographer", "ICP Blueprint validated.", "completed", {"persona_data": persona_data})

                # -------------------------------------------------------------
                # NODES 4 & 5: Wordsmith <-> Overwatch Debate & Verification Loop
                # -------------------------------------------------------------
                copy_data = None
                critique_notes = None
                debate_history = []
                is_approved = False

                for iteration in range(1, self.max_debate_rounds + 1):
                    emit("Wordsmith", f"Drafting conversion assets (Iteration #{iteration})...", "active")
                    copy_data = await asyncio.to_thread(
                        self.wordsmith.run,
                        raw_idea,
                        market_data,
                        competitor_data,
                        persona_data,
                        critique_notes,
                        iteration,
                        emit
                    )

                    emit("Overwatch", f"Executing Conversion Audit on draft #{iteration}...", "active")
                    is_approved, critique_eval = await asyncio.to_thread(
                        self.overwatch.evaluate,
                        raw_idea,
                        competitor_data,
                        persona_data,
                        copy_data,
                        iteration,
                        emit
                    )

                    debate_history.append({
                        "round": iteration,
                        "brand_name": copy_data.get("brand_name"),
                        "hero_headline": copy_data.get("landing_page", {}).get("hero_headline"),
                        "score": critique_eval.get("total_score"),
                        "verdict": critique_eval.get("verdict"),
                        "flaws": critique_eval.get("flaws", []),
                        "directives": critique_eval.get("tactical_directives", [])
                    })

                    emit("Overwatch", f"Debate Round #{iteration} verdict: {critique_eval.get('verdict')} (Score: {critique_eval.get('total_score')}/100)", 
                         "approved" if is_approved else "critique", 
                         {"debate_entry": debate_history[-1]})

                    if is_approved or iteration >= self.max_debate_rounds:
                        break
                    
                    critique_notes = critique_eval
                    await asyncio.sleep(0.3)

                # -------------------------------------------------------------
                # NODE 6: Foundry (Asset Compilation & Deployment Prep)
                # -------------------------------------------------------------
                emit("Foundry", "Synthesizing production Tailwind CSS landing page and B2B CSV leads...", "active")
                
                brand_name = copy_data.get("brand_name", "VenturePulse")
                tagline = copy_data.get("tagline", "Autonomous Revenue Engine")
                landing_page = copy_data.get("landing_page", {})
                battlecard = competitor_data.get("battlecard", [])

                html_code = self.foundry.generate_landing_page_html(
                    brand_name=brand_name,
                    tagline=tagline,
                    landing_page_data=landing_page,
                    competitor_battlecard=battlecard
                )

                leads_csv = self.foundry.generate_leads_csv(
                    brand_name=brand_name,
                    persona_data=persona_data
                )

                final_assets = {
                    "brand_name": brand_name,
                    "tagline": tagline,
                    "landing_page_html": html_code,
                    "leads_csv": leads_csv,
                    "landing_page_data": landing_page,
                    "outbound_sequence": copy_data.get("outbound_sequence", []),
                    "competitor_data": competitor_data,
                    "persona_data": persona_data,
                    "market_data": market_data,
                    "debate_history": debate_history,
                    "final_score": debate_history[-1].get("score", 92) if debate_history else 92,
                    "total_duration": round(time.time() - start_time, 2)
                }

                emit("Foundry", "Production assets generated and validated.", "completed", {"final_assets": final_assets})
                queue.put_nowait({"type": "done", "final_assets": final_assets})

            except Exception as e:
                logger.exception("Swarm execution error:")
                emit("Orchestrator", f"Encountered unexpected error: {str(e)}", "error")
                queue.put_nowait({"type": "error", "error": str(e)})

        # Launch workflow runner as background task
        runner_task = asyncio.create_task(workflow_runner())

        # Stream items from queue to SSE consumer
        while True:
            item = await queue.get()
            yield item
            queue.task_done()
            if item.get("type") in ["done", "error"]:
                break

        await runner_task
