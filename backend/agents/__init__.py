"""Research agents package."""

from backend.agents.manager import ResearchManagerAgent
from backend.agents.evidence_agent import EvidenceExtractionAgent
from backend.agents.critic_agent import CriticAgent

__all__ = ["ResearchManagerAgent", "EvidenceExtractionAgent", "CriticAgent"]
