from backend.config import Config
from backend.models.research import ResearchPlan
from backend.agents.evidence_agent import EvidenceExtractionAgent


def test_extract_evidence_returns_structured_claims():
    config = Config(GOOGLE_API_KEY="", GEMINI_MODEL="gemini-2.0-flash")
    agent = EvidenceExtractionAgent(config)

    plan = ResearchPlan(
        question="Will AI replace software developers by 2030?",
        complexity="complex",
        research_goals=[
            "Understand current AI coding capabilities",
            "Assess productivity and labor market effects",
            "Evaluate technical and organizational limitations",
        ],
        subquestions=[
            "What can current AI coding systems actually do?",
            "How do AI tools affect developer productivity?",
            "What are the main limitations of AI coding systems?",
            "What do labor market and expert analyses suggest?",
        ],
        expected_sources=[
            "Academic papers",
            "Technical reports",
            "Industry reports",
            "Expert analysis",
        ],
        estimated_timeline="2-3 weeks",
        research_strategy="Gather primary evidence from academic, policy, and industry sources and evaluate conflicting viewpoints.",
        success_criteria=[
            "At least 3 high-quality sources",
            "Evidence from multiple source types",
            "Clear identification of conflicting claims",
        ],
    )

    sources = [
        {
            "title": "AI coding assistants boost developer productivity in controlled studies",
            "url": "https://example.com/ai-productivity-study",
            "publisher": "Research Lab",
            "publication_date": "2024-05-15",
            "source_type": "academic",
            "relevance_score": 96,
            "reason_for_relevance": "Directly studies developer productivity gains from AI coding tools.",
        },
        {
            "title": "Labor market analysts warn that AI will reshape software work, not eliminate it",
            "url": "https://example.com/labor-market-analysis",
            "publisher": "Industry analyst",
            "publication_date": "2024-07-01",
            "source_type": "industry_report",
            "relevance_score": 91,
            "reason_for_relevance": "Covers workforce implications and likely automation effects.",
        },
        {
            "title": "AI systems still struggle with long-running software tasks and debugging reliability",
            "url": "https://example.com/ai-limitations",
            "publisher": "Technical review",
            "publication_date": "2023-11-22",
            "source_type": "technical",
            "relevance_score": 88,
            "reason_for_relevance": "Highlights constraints that limit full automation of developer work.",
        },
    ]

    evidence = agent.extract_evidence(plan, sources)

    assert isinstance(evidence, list)
    assert len(evidence) >= 3

    for item in evidence:
        assert "claim" in item
        assert "evidence_type" in item
        assert "supporting_sources" in item
        assert "confidence" in item
        assert item["confidence"] in {"low", "medium", "high"}
        assert item["supporting_sources"]
