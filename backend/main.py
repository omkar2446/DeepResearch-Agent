"""Main entry point for DeepResearch Agent."""

import logging
import sys
from datetime import datetime

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


if __name__ == "__main__":
    sys.exit(main())

