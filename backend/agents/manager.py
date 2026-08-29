"""Research Manager Agent - orchestrates the research workflow."""

import logging
from typing import Optional
import json
import re
from datetime import datetime

import google.generativeai as genai

from backend.models.research import ResearchPlan, ResearchProject
from backend.config import Config

logger = logging.getLogger(__name__)


class ResearchManagerAgent:
    """
    The Research Manager Agent is the orchestrator.
    
    It receives research questions and creates structured research plans.
    In later phases, it will delegate work to specialized agents.
    """
    
    def __init__(self, config: Config):
        self.config = config
        genai.configure(api_key=config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)
        logger.info(f"ResearchManagerAgent initialized with model: {config.GEMINI_MODEL}")
    
    def create_research_plan(self, research_question: str) -> ResearchPlan:
        """
        Create a structured research plan for the given question.
        
        Args:
            research_question: The research question to analyze.
            
        Returns:
            ResearchPlan: A structured research plan.
        """
        logger.info(f"Creating research plan for: {research_question}")
        
        prompt = self._build_planning_prompt(research_question)
        
        try:
            response = self.model.generate_content(prompt)
            plan_text = response.text
            logger.debug(f"Raw response from Gemini:\n{plan_text}")
            
            # Extract JSON from the response
            plan_json = self._extract_json_from_response(plan_text)
            
            # Parse into ResearchPlan model
            plan = ResearchPlan(**plan_json)
            logger.info(f"Successfully created research plan with {len(plan.subquestions)} subquestions")
            
            return plan
            
        except Exception as e:
            logger.error(f"Error creating research plan: {e}")
            raise
    
    def create_research_project(self, research_question: str, plan: ResearchPlan) -> ResearchProject:
        """
        Create a research project document.
        
        Args:
            research_question: The research question.
            plan: The research plan.
            
        Returns:
            ResearchProject: A research project document.
        """
        import uuid
        
        research_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        project = ResearchProject(
            research_id=research_id,
            question=research_question,
            status="planning",
            plan=plan,
            created_at=now,
            updated_at=now,
            monitoring_enabled=False,
        )
        
        logger.info(f"Created research project: {research_id}")
        return project
    
    def _build_planning_prompt(self, research_question: str) -> str:
        """Build the prompt for research planning."""
        
        prompt = f"""You are a senior research analyst and strategic researcher.

Your task is to create a comprehensive research plan for investigating the following question:

RESEARCH QUESTION:
{research_question}

Analyze this question deeply and create a structured research plan.

Your response MUST be a valid JSON object with EXACTLY this structure:
{{
  "question": "{research_question}",
  "complexity": "simple|moderate|complex",
  "research_goals": ["goal1", "goal2", "goal3"],
  "subquestions": ["subquestion1", "subquestion2", ...],
  "expected_sources": ["Academic papers", "Industry reports", ...],
  "estimated_timeline": "estimated duration",
  "research_strategy": "brief description of research approach",
  "success_criteria": ["criterion1", "criterion2", ...]
}}

Requirements:

1. COMPLEXITY: Assess whether this is simple (can be answered with basic facts), moderate (requires synthesis of multiple sources), or complex (requires deep analysis and expert synthesis).

2. RESEARCH_GOALS: List 3-5 specific research goals that directly address the question.

3. SUBQUESTIONS: Break down the main question into 5-8 specific subquestions that collectively address the research goals. Each subquestion should be specific and researchable.

4. EXPECTED_SOURCES: List types of sources that would be most relevant (e.g., "Academic papers on battery technology", "Industry analyst reports").

5. ESTIMATED_TIMELINE: Give a realistic timeline for completing this research.

6. RESEARCH_STRATEGY: Describe your high-level approach to answering this question.

7. SUCCESS_CRITERIA: Define 4-6 criteria for determining whether the research has been successful.

IMPORTANT:
- Return ONLY valid JSON, no additional text before or after.
- All strings must be valid JSON strings (properly escaped).
- All arrays must contain strings.
- Do not use markdown formatting.
- Do not include explanatory text outside the JSON.
"""
        
        return prompt
    
    def _extract_json_from_response(self, response_text: str) -> dict:
        """
        Extract JSON from Gemini response.
        
        Gemini sometimes wraps JSON in markdown code blocks.
        This method handles various formats.
        """
        
        # Try to extract JSON from markdown code blocks first
        json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # If no code block, try to find JSON object
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response_text
        
        # Parse the JSON
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {json_str}")
            raise ValueError(f"Failed to parse Gemini response as JSON: {e}")
