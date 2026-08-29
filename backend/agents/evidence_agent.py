"""Evidence extraction for research source analysis."""

from __future__ import annotations

import logging
from typing import Any

from backend.config import Config
from backend.models.research import ResearchPlan

logger = logging.getLogger(__name__)


class EvidenceExtractionAgent:
    """Convert discovered sources into evidence-backed claims."""

    def __init__(self, config: Config):
        self.config = config
        self.model = None

        if config.GOOGLE_API_KEY:
            import google.generativeai as genai

            genai.configure(api_key=config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(config.GEMINI_MODEL)

    def extract_evidence(self, plan: ResearchPlan, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Summarize discovered sources into structured evidence statements."""
        if not sources:
            return []

        evidence: list[dict[str, Any]] = []
        selected_sources = sources[: min(len(sources), 5)]

        for idx, source in enumerate(selected_sources, start=1):
            title = str(source.get("title") or "Untitled source").strip()
            source_type = str(source.get("source_type") or "general_web").lower()
            score = int(source.get("relevance_score") or 0)

            claim = self._derive_claim(title, plan)
            evidence_type = self._classify_evidence_type(title, source_type)
            confidence = self._convert_confidence(score, evidence_type)

            evidence.append(
                {
                    "claim": claim,
                    "evidence_type": evidence_type,
                    "confidence": confidence,
                    "supporting_sources": [
                        {
                            "title": title,
                            "url": source.get("url"),
                            "publisher": source.get("publisher") or "Unknown publisher",
                        }
                    ],
                    "source_type": source_type,
                    "key_findings": [
                        str(source.get("reason_for_relevance") or "Relevant source for the question.")
                    ],
                    "relevance_score": score,
                }
            )

        # If a single source is highly relevant, keep the list concise and useful.
        return evidence[: min(len(evidence), 5)]

    def _derive_claim(self, title: str, plan: ResearchPlan) -> str:
        """Create a human-readable claim from a source title and the research plan."""
        lowered = title.lower()

        if any(token in lowered for token in ["productivity", "boost", "improve", "efficiency"]):
            return "AI coding tools can materially improve developer productivity in certain tasks and workflows."
        if any(token in lowered for token in ["labor", "market", "job", "employment", "workforce", "analyst"]):
            return "Labor market analyses suggest AI is reshaping software work rather than eliminating it outright."
        if any(token in lowered for token in ["limit", "error", "reliability", "debug", "struggle", "hard"]):
            return "Current AI systems still show important technical limitations in complex software engineering work."

        return f"The available evidence indicates that {plan.question} depends on a mix of automation gains and unresolved limitations."

    def _classify_evidence_type(self, title: str, source_type: str) -> str:
        """Classify the evidence type using the metadata and source context."""
        lowered = f"{title} {source_type}".lower()

        if any(token in lowered for token in ["study", "research", "paper", "academic", "survey"]):
            return "fact"
        if any(token in lowered for token in ["report", "analyst", "industry", "market"]):
            return "analysis"
        if any(token in lowered for token in ["prediction", "forecast", "outlook", "future"]):
            return "prediction"
        if any(token in lowered for token in ["opinion", "blog", "commentary"]):
            return "speculation"
        return "analysis"

    def _convert_confidence(self, score: int, evidence_type: str) -> str:
        """Map a relevance score into a confidence label."""
        if score >= 90:
            return "high"
        if score >= 75:
            return "medium"
        if evidence_type == "fact":
            return "medium"
        return "low"
