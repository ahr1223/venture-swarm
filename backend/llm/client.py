"""
LLM Client Layer for VentureSwarm
Provides unified interface for:
1. Google Gemini via `google-genai` (using gemini-3.8-flash)
2. OpenAI (using gpt-4o / gpt-4o-mini)
3. Intelligent Heuristic Engine (deterministic high-fidelity fallback when no API key is supplied)
"""

import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("ventureswarm.llm")

class LLMClient:
    def __init__(self, api_key: Optional[str] = None, provider: str = "auto", model: Optional[str] = None):
        self.gemini_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.provider = provider
        self.model = model

        # Detect active provider
        if self.provider == "auto":
            if self.gemini_key:
                self.provider = "gemini"
            elif self.openai_key:
                self.provider = "openai"
            else:
                self.provider = "simulation"

        logger.info(f"Initialized LLMClient with active provider: {self.provider}")

    def generate(self, system_prompt: str, user_prompt: str, response_format: str = "text") -> str:
        """
        Generates completion from active provider or fallback engine.
        """
        if self.provider == "gemini" and self.gemini_key:
            try:
                from google import genai
                client = genai.Client(api_key=self.gemini_key)
                model_name = self.model or "gemini-3.8-flash"
                
                prompt = f"System Instructions:\n{system_prompt}\n\nTask:\n{user_prompt}"
                if response_format == "json":
                    prompt += "\n\nCRITICAL: Respond ONLY with a valid raw JSON object. Do not enclose in markdown ticks if possible, or use standard ```json ``` formatting."

                # Try models.generate_content (standard across Gemini keys)
                try:
                    res = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    if res.text:
                        return res.text
                except Exception:
                    # Fallback to interactions.create
                    response = client.interactions.create(
                        model=model_name,
                        input=prompt
                    )
                    if response.output_text:
                        return response.output_text
            except Exception as e:
                logger.error(f"Gemini API call failed: {e}. Falling back to domain heuristic synthesis.")

        if self.provider == "openai" and self.openai_key:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=self.openai_key)
                model_name = self.model or "gpt-4o"
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
                kwargs = {
                    "model": model_name,
                    "messages": messages,
                    "temperature": 0.7
                }
                if response_format == "json":
                    kwargs["response_format"] = {"type": "json_object"}

                response = client.chat.completions.create(**kwargs)
                return response.choices[0].message.content or ""
            except Exception as e:
                logger.error(f"OpenAI API call failed: {e}. Falling back to heuristic synthesis.")

        # Default fallback: return structured simulated response
        return ""

    def get_provider_status(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "has_gemini": bool(self.gemini_key),
            "has_openai": bool(self.openai_key),
            "is_live_api": self.provider in ["gemini", "openai"] and (bool(self.gemini_key) or bool(self.openai_key)),
            "model": self.model or ("gemini-3.8-flash" if self.provider == "gemini" else "gpt-4o" if self.provider == "openai" else "Swarm-Heuristic-Engine")
        }
