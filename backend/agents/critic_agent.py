"""Critic Agent - validates and challenges research evidence."""

from __future__ import annotations

import logging
from typing import Any

from backend.config import Config
from backend.models.research import ResearchPlan

logger = logging.getLogger(__name__)


class CriticAgent:
    """Validate evidence, identify contradictions, and assess confidence levels."""

    def __init__(self, config: Config):
        self.config = config
        self.model = None

        if config.GOOGLE_API_KEY:
            import google.generativeai as genai

            genai.configure(api_key=config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(config.GEMINI_MODEL)

    def critique_evidence(self, plan: ResearchPlan, evidence: list[dict[str, Any]]) -> dict[str, Any]:
        """Analyze evidence for gaps, contradictions, and confidence levels."""
        if not evidence:
            return {
                "summary": "No evidence provided for critique.",
                "contradictions": [],
                "gaps": [],
                "confidence_assessment": "very_low",
                "needs_more_research": True,
            }

        contradictions = self._detect_contradictions(evidence)
        gaps = self._identify_gaps(plan, evidence)
        confidence = self._assess_confidence(evidence, contradictions)
        needs_more = len(gaps) > 0 or len(contradictions) > 1 or confidence == "low"

        summary = self._generate_summary(plan, evidence, contradictions, gaps, confidence)

        return {
            "summary": summary,
            "contradictions": contradictions,
            "gaps": gaps,
            "confidence_assessment": confidence,
            "needs_more_research": needs_more,
            "total_evidence_items": len(evidence),
            "high_confidence_sources": sum(1 for e in evidence if e.get("confidence") == "high"),
        }

    def _detect_contradictions(self, evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Identify conflicting claims within the evidence set."""
        contradictions = []

        claims_by_category = {}
        for item in evidence:
            claim_category = self._extract_category(item.get("claim", ""))
            if claim_category not in claims_by_category:
                claims_by_category[claim_category] = []
            claims_by_category[claim_category].append(item)

        for category, items in claims_by_category.items():
            if len(items) > 1:
                evidence_types = set(e.get("evidence_type") for e in items)
                if len(evidence_types) > 1 or any(e.get("evidence_type") == "speculation" for e in items):
                    contradictions.append(
                        {
                            "category": category,
                            "conflicting_claims": [e.get("claim") for e in items],
                            "severity": "low" if len(items) == 2 else "medium",
                        }
                    )

        return contradictions

    def _identify_gaps(self, plan: ResearchPlan, evidence: list[dict[str, Any]]) -> list[str]:
        """Identify missing evidence or unaddressed subquestions."""
        gaps = []
        evidence_claims = " ".join(e.get("claim", "") for e in evidence).lower()

        for subq in plan.subquestions:
            subq_lower = subq.lower()
            key_terms = [word for word in subq_lower.split() if len(word) > 4]
            coverage = sum(1 for term in key_terms if term in evidence_claims)

            if coverage < len(key_terms) * 0.5:
                gaps.append(f"Insufficient evidence for: {subq}")

        if not any("limitation" in e.get("claim", "").lower() for e in evidence):
            gaps.append("Missing evidence on technical limitations and constraints.")

        if not any("market" in e.get("claim", "").lower() or "employment" in e.get("claim", "").lower() for e in evidence):
            gaps.append("Missing labor market or economic impact evidence.")

        return gaps[:5]

    def _assess_confidence(self, evidence: list[dict[str, Any]], contradictions: list) -> str:
        """Determine overall confidence level based on evidence quality and consistency."""
        if not evidence:
            return "very_low"

        high_confidence_count = sum(1 for e in evidence if e.get("confidence") == "high")
        confidence_ratio = high_confidence_count / len(evidence)

        source_types = set(e.get("source_type") for e in evidence)
        type_diversity = len(source_types)

        if contradictions and len(contradictions) > 1:
            return "low"
        if confidence_ratio >= 0.66 and type_diversity >= 2:
            return "high"
        if confidence_ratio >= 0.4 and type_diversity >= 2:
            return "medium"
        if confidence_ratio >= 0.5:
            return "medium"
        return "low"

    def _generate_summary(
        self, plan: ResearchPlan, evidence: list[dict[str, Any]], contradictions: list, gaps: list, confidence: str
    ) -> str:
        """Generate a human-readable summary of the critique."""
        parts = [
            f"Analyzed {len(evidence)} evidence items addressing the question: {plan.question}",
            f"Overall confidence: {confidence.upper()}.",
        ]

        if contradictions:
            parts.append(f"Found {len(contradictions)} area(s) of conflicting evidence that need reconciliation.")
        else:
            parts.append("Evidence is internally consistent with no major contradictions detected.")

        if gaps:
            parts.append(f"Identified {len(gaps)} evidence gap(s) requiring additional research.")

        source_types = set(e.get("source_type") for e in evidence)
        if len(source_types) >= 3:
            parts.append("Evidence spans multiple high-quality source types (academic, industry, technical).")
        else:
            parts.append("Evidence coverage could benefit from additional source types.")

        return " ".join(parts)

    def _extract_category(self, claim: str) -> str:
        """Extract a category label from a claim for grouping."""
        claim_lower = claim.lower()
        if "productivity" in claim_lower or "improve" in claim_lower:
            return "capability"
        if "limit" in claim_lower or "constraint" in claim_lower:
            return "limitation"
        if "market" in claim_lower or "employment" in claim_lower or "job" in claim_lower:
            return "labor_market"
        if "legal" in claim_lower or "security" in claim_lower or "liability" in claim_lower:
            return "risk"
        return "general"
