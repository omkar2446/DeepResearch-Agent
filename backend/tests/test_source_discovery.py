from backend.config import Config
from backend.models.research import ResearchPlan
from backend.agents.search_agent import SourceDiscoveryAgent


def test_discover_sources_returns_structured_results():
    config = Config(GOOGLE_API_KEY="", GEMINI_MODEL="gemini-2.0-flash")
    agent = SourceDiscoveryAgent(config)

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

    results = agent.discover_sources(plan.question, plan)

    assert isinstance(results, list)
    assert len(results) >= 3

    for source in results:
        assert "title" in source
        assert "url" in source
        assert source["url"].startswith("http")
        assert "source_type" in source
        assert "relevance_score" in source
        assert 0 <= source["relevance_score"] <= 100
        assert "reason_for_relevance" in source
        assert "publisher" in source
