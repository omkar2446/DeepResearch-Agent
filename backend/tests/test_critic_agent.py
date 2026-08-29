from backend.config import Config
from backend.models.research import ResearchPlan
from backend.agents.critic_agent import CriticAgent


def test_critic_validates_evidence_and_returns_review():
    config = Config(GOOGLE_API_KEY="", GEMINI_MODEL="gemini-3.6-flash")
    agent = CriticAgent(config)

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

    evidence = [
        {
            "claim": "AI coding tools can materially improve developer productivity in certain tasks and workflows.",
            "evidence_type": "fact",
            "confidence": "high",
            "supporting_sources": [
                {
                    "title": "AI coding assistants boost developer productivity in controlled studies",
                    "url": "https://example.com/ai-productivity-study",
                    "publisher": "Research Lab",
                }
            ],
            "source_type": "academic",
            "key_findings": ["Directly studies developer productivity gains from AI coding tools."],
            "relevance_score": 96,
        },
        {
            "claim": "Labor market analyses suggest AI is reshaping software work rather than eliminating it outright.",
            "evidence_type": "analysis",
            "confidence": "high",
            "supporting_sources": [
                {
                    "title": "Labor market analysts warn that AI will reshape software work, not eliminate it",
                    "url": "https://example.com/labor-market-analysis",
                    "publisher": "Industry analyst",
                }
            ],
            "source_type": "industry_report",
            "key_findings": ["Covers workforce implications and likely automation effects."],
            "relevance_score": 91,
        },
        {
            "claim": "Current AI systems still show important technical limitations in complex software engineering work.",
            "evidence_type": "fact",
            "confidence": "medium",
            "supporting_sources": [
                {
                    "title": "AI systems still struggle with long-running software tasks and debugging reliability",
                    "url": "https://example.com/ai-limitations",
                    "publisher": "Technical review",
                }
            ],
            "source_type": "technical",
            "key_findings": ["Highlights constraints that limit full automation of developer work."],
            "relevance_score": 88,
        },
    ]

    review = agent.critique_evidence(plan, evidence)

    assert isinstance(review, dict)
    assert "summary" in review
    assert "contradictions" in review
    assert "gaps" in review
    assert "confidence_assessment" in review
    assert "needs_more_research" in review
    assert isinstance(review["contradictions"], list)
    assert isinstance(review["gaps"], list)
    assert isinstance(review["needs_more_research"], bool)
