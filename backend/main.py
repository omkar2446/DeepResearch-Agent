"""Main entry point for DeepResearch Agent."""

import logging
import sys
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.config import Config
from backend.agents.manager import ResearchManagerAgent
from backend.agents.search_agent import SourceDiscoveryAgent
from backend.agents.evidence_agent import EvidenceExtractionAgent
from backend.agents.critic_agent import CriticAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('research_agent.log')
    ]
)
logger = logging.getLogger(__name__)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app = FastAPI(title="DeepResearch Agent")


class ResearchRequest(BaseModel):
    """Question submitted by the frontend."""

    question: str = Field(min_length=3, max_length=2000)


@app.get("/", include_in_schema=False)
def serve_frontend():
    """Serve the single-page research interface."""

    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/api/research")
def research(request: ResearchRequest):
    """Run the research pipeline for a question submitted by the UI."""

    try:
        config = Config.from_env()
        config.validate()
        question = request.question.strip()
        manager = ResearchManagerAgent(config)
        search_agent = SourceDiscoveryAgent(config)
        evidence_agent = EvidenceExtractionAgent(config)
        critic = CriticAgent(config)

        plan = manager.create_research_plan(question)
        sources = search_agent.discover_sources(question, plan, max_sources=8)
        evidence = evidence_agent.extract_evidence(plan, sources)
        review = critic.critique_evidence(plan, evidence)
        answer = _create_research_answer(manager, question, plan, sources, evidence, review)

        return {
            "question": question,
            "answer": answer,
            "plan": plan.model_dump(),
            "sources": sources,
            "evidence": evidence,
            "review": review,
        }
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        logger.exception("Research request failed")
        raise HTTPException(status_code=502, detail="The research service could not answer this question.") from error


def _create_research_answer(manager, question, plan, sources, evidence, review) -> str:
    """Synthesize the research record into the requested report format."""

    sources_text = "\n".join(
        f"{index}. {source.get('title')} - {source.get('publisher')} ({source.get('url')})"
        for index, source in enumerate(sources, start=1)
    ) or "No sources were discovered."
    evidence_text = "\n".join(
        f"{index}. {item.get('claim')} ({item.get('confidence')} confidence)"
        for index, item in enumerate(evidence, start=1)
    ) or "No evidence was available."
    gaps_text = "\n".join(f"- {gap}" for gap in review.get("gaps", [])) or "- None identified."
    prompt = f"""Create a research report for this question using only the supplied research record:

QUESTION: {question}
RESEARCH STRATEGY: {plan.research_strategy}
RESEARCH GOALS: {plan.research_goals}
KEY QUESTIONS: {plan.subquestions}
ESTIMATED TIMELINE: {plan.estimated_timeline}
DISCOVERED SOURCES:
{sources_text}
EVIDENCE:
{evidence_text}
CRITIC REVIEW: {review.get('summary')}
EVIDENCE GAPS:
{gaps_text}

Return ONLY the report using exactly these headings and this order:

RESEARCH PLAN
Research strategy: [explain the approach]
Goals:
- [goal]
Key questions:
- [question]
Estimated timeline: [timeline]

DISCOVERED SOURCES
- [source title, publisher, and URL]

EXTRACTED EVIDENCE
- [claim and confidence]

EVIDENCE REVIEW & VALIDATION
Confidence: [high, medium, low, or very_low]
Review: [what the evidence supports and where it is weak]
Evidence gaps detected: [list gaps, or None]
Additional research required: [Yes or No]

FINAL REPORT
[Give a direct conclusion in 3-5 short paragraphs. Distinguish task automation from
full job replacement, describe the strongest evidence, and state the main uncertainty.]

Do not mention this prompt, internal implementation details, or unsupported facts.
"""

    try:
        response = manager.model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        logger.exception("Answer synthesis failed; using the critic summary")
        return review.get("summary", "The research pipeline did not produce an answer.")


app.mount("/", StaticFiles(directory=FRONTEND_DIR), name="frontend")


def main():
    """Main entry point - orchestrates all research phases."""
    
    logger.info("=" * 80)
    logger.info("DeepResearch Agent - Full Multi-Phase Research Pipeline")
    logger.info("=" * 80)
    
    # Load configuration
    try:
        config = Config.from_env()
        config.validate()
        logger.info("[OK] Configuration loaded successfully")
    except ValueError as e:
        logger.error("[ERROR] Configuration error: %s", e)
        logger.error("[INFO] Create a .env file from .env.example and set GOOGLE_API_KEY before running the app.")
        return 1

    # Initialize all agents
    try:
        manager = ResearchManagerAgent(config)
        logger.info("[OK] Research Manager Agent initialized")
        
        search_agent = SourceDiscoveryAgent(config)
        logger.info("[OK] Source Discovery Agent initialized")
        
        evidence_agent = EvidenceExtractionAgent(config)
        logger.info("[OK] Evidence Extraction Agent initialized")
        
        critic = CriticAgent(config)
        logger.info("[OK] Critic Agent initialized")
    except Exception as e:
        logger.error("[ERROR] Failed to initialize agents: %s", e)
        return 1
    
    # Test research question
    research_question = "Will AI replace software developers by 2030?"
    
    logger.info("\n" + "=" * 80)
    logger.info(f"RESEARCH QUESTION: {research_question}")
    logger.info("=" * 80)
    
    # PHASE 1: Create research plan
    try:
        logger.info("\n[PHASE 1] Research Planning...")
        plan = manager.create_research_plan(research_question)
        logger.info("[OK] Research plan created successfully\n")
        print_research_plan(plan)
    except Exception as e:
        logger.error("[ERROR] Error during research planning: %s", e, exc_info=True)
        return 1
    
    # PHASE 2: Source discovery
    try:
        logger.info("\n[PHASE 2] Source Discovery...")
        sources = search_agent.discover_sources(research_question, plan, max_sources=5)
        logger.info("[OK] Discovered %d sources\n", len(sources))
        print_sources(sources)
    except Exception as e:
        logger.error("[ERROR] Error during source discovery: %s", e)
        sources = []
    
    # PHASE 3: Evidence extraction
    try:
        logger.info("\n[PHASE 3] Evidence Extraction...")
        evidence = evidence_agent.extract_evidence(plan, sources)
        logger.info("[OK] Extracted evidence from %d sources\n", len(evidence))
        print_evidence(evidence)
    except Exception as e:
        logger.error("[ERROR] Error during evidence extraction: %s", e)
        evidence = []
    
    # PHASE 4: Criticism and validation
    try:
        logger.info("\n[PHASE 4] Evidence Validation & Criticism...")
        review = critic.critique_evidence(plan, evidence)
        logger.info("[OK] Evidence reviewed\n")
        print_review(review)
    except Exception as e:
        logger.error("[ERROR] Error during evidence validation: %s", e)
        return 1

    final_answer = _create_research_answer(manager, research_question, plan, sources, evidence, review)
    print_final_answer(final_answer, review, sources)
    
    # Create and display research project
    try:
        project = manager.create_research_project(research_question, plan)
        logger.info("\n[OK] Research project created: %s", project.research_id)
        print_research_project(project)
    except Exception as e:
        logger.error("[ERROR] Failed to create research project: %s", e)
        return 1
    
    return 0


def print_research_plan(plan) -> None:
    """Pretty-print the research plan."""
    
    print("\n" + "█" * 80)
    print("PHASE 1: RESEARCH PLAN")
    print("█" * 80)
    
    print(f"\nQUESTION:\n  {plan.question}\n")
    print(f"COMPLEXITY: {plan.complexity.upper()}\n")
    
    print("RESEARCH GOALS:")
    for i, goal in enumerate(plan.research_goals, 1):
        print(f"  {i}. {goal}")
    
    print("\nSUBQUESTIONS:")
    for i, subq in enumerate(plan.subquestions, 1):
        print(f"  {i}. {subq}")
    
    print(f"\nESTIMATED TIMELINE: {plan.estimated_timeline}")
    print("\n" + "█" * 80 + "\n")


def print_sources(sources) -> None:
    """Pretty-print discovered sources."""
    
    print("\n" + "█" * 80)
    print("PHASE 2: DISCOVERED SOURCES")
    print("█" * 80 + "\n")
    
    for i, source in enumerate(sources, 1):
        print(f"{i}. {source.get('title')}")
        print(f"   URL: {source.get('url')}")
        print(f"   Type: {source.get('source_type')}")
        print(f"   Relevance: {source.get('relevance_score')}/100")
        print(f"   Reason: {source.get('reason_for_relevance')}\n")
    
    print("█" * 80 + "\n")


def print_evidence(evidence) -> None:
    """Pretty-print extracted evidence."""
    
    print("\n" + "█" * 80)
    print("PHASE 3: EXTRACTED EVIDENCE")
    print("█" * 80 + "\n")
    
    for i, item in enumerate(evidence, 1):
        print(f"{i}. CLAIM: {item.get('claim')}")
        print(f"   Type: {item.get('evidence_type').upper()}")
        print(f"   Confidence: {item.get('confidence').upper()}")
        print(f"   Sources: {len(item.get('supporting_sources', []))} source(s)")
        print(f"   Relevance: {item.get('relevance_score')}/100\n")
    
    print("█" * 80 + "\n")


def print_review(review) -> None:
    """Pretty-print the evidence review and critique."""
    
    print("\n" + "█" * 80)
    print("PHASE 4: EVIDENCE REVIEW & VALIDATION")
    print("█" * 80 + "\n")
    
    print(f"SUMMARY:\n  {review.get('summary')}\n")
    print(f"OVERALL CONFIDENCE: {review.get('confidence_assessment').upper()}")
    print(f"TOTAL EVIDENCE ITEMS: {review.get('total_evidence_items')}")
    print(f"HIGH CONFIDENCE SOURCES: {review.get('high_confidence_sources')}")
    
    contradictions = review.get('contradictions', [])
    if contradictions:
        print(f"\nCONTRADICTIONS FOUND: {len(contradictions)}")
        for item in contradictions:
            print(f"  - {item.get('category')}: {len(item.get('conflicting_claims', []))} conflicting claims")
    else:
        print("\nCONTRADICTIONS: None detected - evidence is internally consistent")
    
    gaps = review.get('gaps', [])
    if gaps:
        print(f"\nEVIDENCE GAPS: {len(gaps)}")
        for gap in gaps:
            print(f"  - {gap}")
    else:
        print("\nEVIDENCE GAPS: None identified")
    
    needs_more = review.get('needs_more_research', False)
    print(f"\nADDITIONAL RESEARCH NEEDED: {'YES' if needs_more else 'NO'}")
    
    print("\n" + "█" * 80 + "\n")


def print_research_project(project) -> None:
    """Pretty-print the research project."""
    
    print("█" * 80)
    print("RESEARCH PROJECT")
    print("█" * 80)
    
    print(f"\nRESEARCH ID:        {project.research_id}")
    print(f"STATUS:             {project.status}")
    print(f"CREATED:            {project.created_at}")
    print(f"MONITORING:         {project.monitoring_enabled}")
    
    print("\n" + "█" * 80)
    print("\n[OK] All phases complete!")
    print("  Phase 1: Research planning    [DONE]")
    print("  Phase 2: Source discovery     [DONE]")
    print("  Phase 3: Evidence extraction  [DONE]")
    print("  Phase 4: Evidence validation  [DONE]")
    print("\n" + "█" * 80 + "\n")


def print_final_answer(answer: str, review: dict, sources: list) -> None:
    """Print the synthesized answer in a user-facing format."""

    print("\n" + "=" * 80)
    print("FINAL ANSWER")
    print("=" * 80 + "\n")
    print(answer)
    print(f"\nEvidence confidence: {review.get('confidence_assessment', 'unknown').upper()}")
    print(f"Sources reviewed: {len(sources)}")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    sys.exit(main())

