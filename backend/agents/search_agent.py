"""Source Discovery Agent for research planning and source collection."""

from __future__ import annotations

import logging
import re
from typing import Any

import google.generativeai as genai
from duckduckgo_search import DDGS

from backend.config import Config
from backend.models.research import ResearchPlan

logger = logging.getLogger(__name__)


class SourceDiscoveryAgent:
    """Find relevant sources for a research question."""

    def __init__(self, config: Config):
        self.config = config
        self.model = None

        if config.GOOGLE_API_KEY:
            genai.configure(api_key=config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(config.GEMINI_MODEL)

    def discover_sources(self, research_question: str, plan: ResearchPlan | None = None, max_sources: int = 8) -> list[dict[str, Any]]:
        """Discover a prioritized list of source candidates for the given question."""
        logger.info("Starting source discovery for: %s", research_question)

        queries = self._build_search_queries(research_question, plan)
        discovered: list[dict[str, Any]] = []
        seen_urls: set[str] = set()

        for query in queries:
            logger.info("Searching query: %s", query)
            results = self._search_web(query)

            for result in results:
                source = self._normalize_source(result, query)
                source_url = source.get("url")

                if not source_url or not source_url.startswith("http"):
                    continue

                if source_url in seen_urls:
                    continue

                seen_urls.add(source_url)
                discovered.append(source)

                if len(discovered) >= max_sources:
                    break

            if len(discovered) >= max_sources:
                break

        if not discovered and self.model:
            logger.info("Web search returned no results. Falling back to Gemini source proposal.")
            discovered = self._discover_sources_via_gemini(research_question, plan or ResearchPlan(
                question=research_question,
                complexity="moderate",
                research_goals=["Understand the issue"],
                subquestions=["What is the core question?"],
                expected_sources=["Primary sources"],
                estimated_timeline="1 week",
                research_strategy="Synthesize available evidence.",
                success_criteria=["Find relevant sources"],
            ))

        if not discovered:
            logger.warning("No sources discovered. Returning a conservative fallback list.")
            discovered = self._default_fallback_sources(research_question)

        logger.info("Discovered %s sources", len(discovered))
        return discovered

    def _build_search_queries(self, research_question: str, plan: ResearchPlan | None) -> list[str]:
        """Build targeted search queries from the research question and plan."""
        base = research_question.strip()
        queries = [base]

        if plan:
            for subquestion in plan.subquestions[:4]:
                if subquestion:
                    queries.append(subquestion)

        # Derive keyword variations focused on evidence and technical review
        keyword_variants = [
            f"{base} evidence",
            f"{base} report",
            f"{base} expert analysis",
            f"{base} academic paper",
        ]

        for variant in keyword_variants:
            if variant not in queries:
                queries.append(variant)

        return queries[:6]

    def _search_web(self, query: str, max_results: int = 3) -> list[dict[str, str]]:
        """Search the web for relevant results without requiring a paid API."""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, region="wt-wt", safesearch="Off", max_results=max_results))
            return results
        except Exception as exc:
            logger.warning("DuckDuckGo search failed for %s: %s", query, exc)
            return []

    def _normalize_source(self, result: dict[str, Any], query: str) -> dict[str, Any]:
        """Normalize arbitrary search results into the expected source schema."""
        title = str(result.get("title") or "Untitled source").strip()
        url = str(result.get("href") or result.get("url") or "").strip()

        # Best-effort publisher extraction from the source string or domain
        publisher = result.get("publisher") or result.get("source") or self._extract_domain(url)

        publication_date = result.get("published") or result.get("date") or "unknown"
        relevance_score = self._score_relevance(title, query)
        reason = (
            f"Relevant to the research question because it discusses the key issue in a searchable, authoritative source context."
        )

        source_type = self._guess_source_type(url, title)

        return {
            "title": title,
            "url": url,
            "publisher": publisher or "Unknown publisher",
            "publication_date": publication_date,
            "source_type": source_type,
            "relevance_score": relevance_score,
            "reason_for_relevance": reason,
        }

    def _guess_source_type(self, url: str, title: str) -> str:
        """Infer likely source category from URL or title."""
        text = f"{url} {title}".lower()

        if any(token in text for token in ["arxiv", "nature", "science", "ieee", "acm", "scholar", "research"]):
            return "academic"
        if any(token in text for token in ["gov", "whitehouse", "nist", "who", "europa", "government"]):
            return "government"
        if any(token in text for token in ["blog", "news", "techcrunch", "reuters", "bloomberg", "wsj", "cnn"]):
            return "journalism"
        if any(token in text for token in ["report", "insights", "analyst", "mckinsey", "gartner", "deloitte"]):
            return "industry_report"
        return "general_web"

    def _score_relevance(self, title: str, query: str) -> int:
        score = 70
        title_lower = title.lower()
        query_words = re.findall(r"[a-zA-Z0-9]+", query.lower())

        overlap = sum(1 for word in query_words if word and word in title_lower)
        score += min(overlap * 5, 25)

        if any(token in title_lower for token in ["report", "study", "paper", "analysis", "survey", "research"]):
            score += 5

        return max(0, min(100, score))

    def _extract_domain(self, url: str) -> str:
        try:
            clean = re.sub(r"^https?://", "", url)
            domain = clean.split("/")[0]
            return domain
        except Exception:
            return "Unknown publisher"

    def _discover_sources_via_gemini(self, research_question: str, plan: ResearchPlan) -> list[dict[str, Any]]:
        """Fallback source discovery using Gemini when web search is unavailable."""
        prompt = (
            f"You are a research source discovery assistant. "
            f"Return ONLY valid JSON as a list of 5 source objects for the following question. "
            f"Each object must contain exactly these keys: title, url, publisher, publication_date, source_type, relevance_score, reason_for_relevance. "
            f"Question: {research_question}\n"
            f"Research goals: {plan.research_goals}\n"
            f"Subquestions: {plan.subquestions}\n"
            f"Return valid JSON only."
        )

        try:
            response = self.model.generate_content(prompt)
            text = response.text
            cleaned = text.strip()
            if "```" in cleaned:
                cleaned = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL).group(1)
            items = __import__("json").loads(cleaned)
            if isinstance(items, dict):
                items = items.get("sources", [])
            return items if isinstance(items, list) else []
        except Exception as exc:
            logger.warning("Gemini source discovery fallback failed: %s", exc)
            return []

    def _default_fallback_sources(self, research_question: str) -> list[dict[str, Any]]:
        """Provide a conservative fallback list when discovery fails."""
        generic_domains = [
            "https://www.nature.com",
            "https://arxiv.org",
            "https://www.mckinsey.com",
            "https://www.gartner.com",
            "https://www.nist.gov",
        ]

        fallback = []
        for idx, url in enumerate(generic_domains, start=1):
            fallback.append({
                "title": f"{research_question} - relevant public research and analysis ({idx})",
                "url": url,
                "publisher": self._extract_domain(url),
                "publication_date": "unknown",
                "source_type": "general_web",
                "relevance_score": 80 - idx,
                "reason_for_relevance": "Fallback source candidate for the research question when live discovery is unavailable.",
            })
        return fallback
