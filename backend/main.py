"""
FastAPI Backend Server for VentureSwarm
Provides real-time SSE streaming for agent swarm execution, export endpoints,
and serves the React frontend interface.
"""

import os
import json
import asyncio
import logging
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, Response, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.agents.orchestrator import SwarmOrchestrator
from backend.llm.client import LLMClient

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("ventureswarm.api")

app = FastAPI(
    title="VentureSwarm API",
    description="Multi-Agent Autonomous Venture Launch Platform",
    version="1.0.0"
)

# Enable CORS for local dev / Vite / React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SwarmLaunchRequest(BaseModel):
    idea: str
    api_key: Optional[str] = None
    provider: Optional[str] = "auto"
    max_debate_rounds: Optional[int] = 2

class ExportHtmlRequest(BaseModel):
    html: str
    filename: Optional[str] = "landing-page.html"

class ExportCsvRequest(BaseModel):
    csv_content: str
    filename: Optional[str] = "target-leads.csv"

@app.get("/api/health")
async def health_check():
    client = LLMClient()
    return {
        "status": "online",
        "service": "VentureSwarm Multi-Agent Engine",
        "provider_status": client.get_provider_status()
    }

@app.post("/api/swarm/stream")
async def stream_swarm_execution(req: SwarmLaunchRequest):
    """
    Server-Sent Events (SSE) streaming endpoint for live multi-agent execution.
    """
    if not req.idea or len(req.idea.strip()) < 3:
        raise HTTPException(status_code=400, detail="Please provide a valid startup idea (minimum 3 characters).")

    orchestrator = SwarmOrchestrator(
        api_key=req.api_key,
        provider=req.provider or "auto",
        max_debate_rounds=req.max_debate_rounds or 2
    )

    async def event_generator():
        try:
            async for event in orchestrator.run_swarm_stream(req.idea):
                data_str = json.dumps(event)
                yield f"data: {data_str}\n\n"
        except Exception as e:
            logger.error(f"SSE stream error: {e}")
            err_data = json.dumps({"type": "error", "error": str(e)})
            yield f"data: {err_data}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@app.post("/api/export/landing-page")
async def export_landing_page(req: ExportHtmlRequest):
    return Response(
        content=req.html,
        media_type="text/html",
        headers={"Content-Disposition": f'attachment; filename="{req.filename}"'}
    )

@app.post("/api/export/leads-csv")
async def export_leads_csv(req: ExportCsvRequest):
    return Response(
        content=req.csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{req.filename}"'}
    )

# Static files / Frontend routing
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")
ASSETS_DIR = os.path.join(STATIC_DIR, "assets")
if os.path.exists(STATIC_DIR):
    # Only mount assets if the directory exists
    if os.path.exists(ASSETS_DIR):
        app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = os.path.join(STATIC_DIR, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))
else:
    # Fallback if dist not built yet: serve standalone rich React HTML client
    STANDALONE_HTML = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "index.html")
    @app.get("/{full_path:path}")
    async def serve_standalone(full_path: str):
        if os.path.exists(STANDALONE_HTML):
            return FileResponse(STANDALONE_HTML)
        return HTMLResponse("<h1>VentureSwarm backend running. Frontend loading...</h1>")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
